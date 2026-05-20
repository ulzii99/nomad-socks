from decimal import Decimal

from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.views import get_or_create_cart
from .models import Order, OrderItem, OrderStatusHistory
from .serializers import CheckoutSerializer, OrderListSerializer, OrderSerializer


class CheckoutView(APIView):
    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        cart = get_or_create_cart(request)
        cart_items = cart.items.select_related("product").all()

        if not cart_items.exists():
            return Response(
                {"error": "Cart is empty."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Calculate totals
        subtotal = sum(item.product.price * item.quantity for item in cart_items)
        shipping_cost = Decimal("0")  # TODO: calculate based on shipping zone
        total = subtotal + shipping_cost

        # Create order
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            guest_email=data["email"],
            guest_name=data["full_name"],
            guest_phone=data["phone"],
            status="pending",
            currency="MNT",
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            total=total,
            shipping_address={
                "full_name": data["full_name"],
                "phone": data["phone"],
                "street_address": data["street_address"],
                "city": data["city"],
                "state_province": data.get("state_province", ""),
                "postal_code": data.get("postal_code", ""),
                "country": data["country"],
            },
            notes=data.get("notes", ""),
        )

        # Create order items (snapshot product data)
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name_en,
                size=item.size,
                quantity=item.quantity,
                unit_price=item.product.price,
                total_price=item.product.price * item.quantity,
            )

        # Record initial status
        OrderStatusHistory.objects.create(
            order=order,
            status="pending",
            note="Order placed",
            created_by=request.user if request.user.is_authenticated else None,
        )

        # Clear cart
        cart.items.all().delete()

        return Response(
            {
                "order_number": order.order_number,
                "total": str(order.total),
                "payment_method": data["payment_method"],
                "status": "pending",
            },
            status=status.HTTP_201_CREATED,
        )


class OrderListView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"error": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        orders = Order.objects.filter(user=request.user)
        serializer = OrderListSerializer(orders, many=True)
        return Response(serializer.data)


class OrderDetailView(APIView):
    def get(self, request, order_number):
        try:
            if request.user.is_authenticated:
                order = Order.objects.get(order_number=order_number, user=request.user)
            else:
                # Guest can view order by number + email
                email = request.query_params.get("email", "")
                order = Order.objects.get(order_number=order_number, guest_email=email)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = OrderSerializer(order)
        return Response(serializer.data)


class AdminOrderListView(APIView):
    """Admin: list all orders with filtering."""
    permission_classes = [IsAdminUser]

    def get(self, request):
        orders = Order.objects.all()
        status_filter = request.query_params.get("status")
        if status_filter:
            orders = orders.filter(status=status_filter)
        serializer = OrderListSerializer(orders, many=True)
        return Response(serializer.data)


class AdminOrderStatusUpdateView(APIView):
    """Admin: update order status."""
    permission_classes = [IsAdminUser]

    def patch(self, request, order_number):
        try:
            order = Order.objects.get(order_number=order_number)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        new_status = request.data.get("status")
        note = request.data.get("note", "")

        valid_statuses = [s[0] for s in Order.STATUS_CHOICES]
        if new_status not in valid_statuses:
            return Response(
                {"error": f"Invalid status. Must be one of: {valid_statuses}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order.status = new_status
        order.save()

        OrderStatusHistory.objects.create(
            order=order,
            status=new_status,
            note=note,
            created_by=request.user,
        )

        serializer = OrderSerializer(order)
        return Response(serializer.data)
