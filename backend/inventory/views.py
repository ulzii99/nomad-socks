from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import ProductSize
from .models import InventoryAdjustment, InventoryRecord, Machine


class InventoryOverviewView(APIView):
    """Admin endpoint: overview of all inventory."""
    permission_classes = [IsAdminUser]

    def get(self, request):
        records = InventoryRecord.objects.select_related(
            "product_size__product"
        ).all()

        data = []
        low_stock = []
        out_of_stock = []

        for record in records:
            item = {
                "product": record.product_size.product.name_en,
                "size": record.product_size.size,
                "sku": record.product_size.sku,
                "quantity": record.quantity_on_hand,
                "threshold": record.low_stock_threshold,
            }
            data.append(item)
            if record.is_out_of_stock:
                out_of_stock.append(item)
            elif record.is_low_stock:
                low_stock.append(item)

        return Response({
            "total_skus": len(data),
            "low_stock_count": len(low_stock),
            "out_of_stock_count": len(out_of_stock),
            "low_stock": low_stock,
            "out_of_stock": out_of_stock,
            "inventory": data,
        })


class InventoryAdjustView(APIView):
    """Admin endpoint: manually adjust inventory."""
    permission_classes = [IsAdminUser]

    def post(self, request):
        sku = request.data.get("sku")
        quantity_change = request.data.get("quantity_change")
        adjustment_type = request.data.get("type", "manual")
        reference = request.data.get("reference", "")

        if not sku or quantity_change is None:
            return Response(
                {"error": "sku and quantity_change are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            product_size = ProductSize.objects.get(sku=sku)
        except ProductSize.DoesNotExist:
            return Response(
                {"error": f"SKU {sku} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        record, _ = InventoryRecord.objects.get_or_create(product_size=product_size)

        new_quantity = record.quantity_on_hand + int(quantity_change)
        if new_quantity < 0:
            return Response(
                {"error": "Cannot reduce below 0."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        record.quantity_on_hand = new_quantity
        record.save()

        InventoryAdjustment.objects.create(
            product_size=product_size,
            adjustment_type=adjustment_type,
            quantity_change=int(quantity_change),
            reference=reference,
            created_by=request.user,
        )

        return Response({
            "sku": sku,
            "quantity_on_hand": record.quantity_on_hand,
            "adjustment": int(quantity_change),
        })


class MachineListView(APIView):
    """Admin endpoint: list machines and their status."""
    permission_classes = [IsAdminUser]

    def get(self, request):
        machines = Machine.objects.all()
        data = [
            {
                "id": m.id,
                "name": m.name,
                "status": m.status,
                "notes": m.notes,
            }
            for m in machines
        ]
        return Response(data)
