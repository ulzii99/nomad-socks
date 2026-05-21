from datetime import timedelta

from django.db.models import Count, Sum, F
from django.utils import timezone
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Order, OrderItem
from inventory.models import InventoryRecord, Machine
from content.models import NewsletterSubscriber


class DashboardView(APIView):
    """Admin dashboard with key metrics."""
    permission_classes = [IsAdminUser]

    def get(self, request):
        now = timezone.now()
        thirty_days_ago = now - timedelta(days=30)
        seven_days_ago = now - timedelta(days=7)

        # Order counts
        all_orders = Order.objects.all()
        orders_30d = all_orders.filter(created_at__gte=thirty_days_ago)
        orders_7d = all_orders.filter(created_at__gte=seven_days_ago)

        # Revenue
        confirmed_statuses = ["confirmed", "processing", "shipped", "delivered"]
        revenue_total = (
            all_orders.filter(status__in=confirmed_statuses)
            .aggregate(total=Sum("total"))["total"] or 0
        )
        revenue_30d = (
            orders_30d.filter(status__in=confirmed_statuses)
            .aggregate(total=Sum("total"))["total"] or 0
        )

        # Order status breakdown
        status_breakdown = dict(
            all_orders.values_list("status").annotate(count=Count("id")).values_list("status", "count")
        )

        # Inventory summary
        inventory_records = InventoryRecord.objects.all()
        total_stock = inventory_records.aggregate(total=Sum("quantity_on_hand"))["total"] or 0
        low_stock_count = sum(1 for r in inventory_records if r.is_low_stock)
        out_of_stock_count = sum(1 for r in inventory_records if r.is_out_of_stock)

        # Machines
        machines = Machine.objects.all()
        active_machines = machines.filter(status="active").count()

        # Subscribers
        subscriber_count = NewsletterSubscriber.objects.filter(is_active=True).count()

        return Response({
            "orders": {
                "total": all_orders.count(),
                "last_30_days": orders_30d.count(),
                "last_7_days": orders_7d.count(),
                "by_status": status_breakdown,
            },
            "revenue": {
                "total": f"{revenue_total:.2f}",
                "last_30_days": f"{revenue_30d:.2f}",
            },
            "inventory": {
                "total_stock": total_stock,
                "total_skus": inventory_records.count(),
                "low_stock": low_stock_count,
                "out_of_stock": out_of_stock_count,
            },
            "machines": {
                "total": machines.count(),
                "active": active_machines,
            },
            "subscribers": subscriber_count,
        })


class TopProductsView(APIView):
    """Top selling products."""
    permission_classes = [IsAdminUser]

    def get(self, request):
        limit = int(request.query_params.get("limit", 10))
        period = request.query_params.get("period", "all")

        items = OrderItem.objects.filter(
            order__status__in=["confirmed", "processing", "shipped", "delivered"]
        )

        if period == "30d":
            items = items.filter(order__created_at__gte=timezone.now() - timedelta(days=30))
        elif period == "7d":
            items = items.filter(order__created_at__gte=timezone.now() - timedelta(days=7))

        top = (
            items.values("product__name_en", "product__id")
            .annotate(
                total_sold=Sum("quantity"),
                total_revenue=Sum("total_price"),
            )
            .order_by("-total_sold")[:limit]
        )

        return Response([
            {
                "product_id": item["product__id"],
                "name": item["product__name_en"],
                "total_sold": item["total_sold"],
                "total_revenue": str(item["total_revenue"]),
            }
            for item in top
        ])


class RevenueReportView(APIView):
    """Revenue by day for the last N days."""
    permission_classes = [IsAdminUser]

    def get(self, request):
        days = int(request.query_params.get("days", 30))
        start_date = timezone.now() - timedelta(days=days)

        orders = (
            Order.objects.filter(
                status__in=["confirmed", "processing", "shipped", "delivered"],
                created_at__gte=start_date,
            )
            .extra(select={"day": "date(created_at)"})
            .values("day")
            .annotate(
                order_count=Count("id"),
                revenue=Sum("total"),
            )
            .order_by("day")
        )

        return Response(list(orders))
