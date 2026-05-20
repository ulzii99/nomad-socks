from rest_framework import serializers

from .models import Order, OrderItem, OrderStatusHistory


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "product", "product_name", "size", "quantity", "unit_price", "total_price"]


class OrderStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatusHistory
        fields = ["status", "note", "created_at"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_history = OrderStatusHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "order_number", "status", "currency", "subtotal",
            "shipping_cost", "total", "shipping_address",
            "notes", "items", "status_history", "created_at",
        ]


class OrderListSerializer(serializers.ModelSerializer):
    item_count = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["order_number", "status", "total", "currency", "item_count", "created_at"]

    def get_item_count(self, obj):
        return obj.items.count()


class CheckoutSerializer(serializers.Serializer):
    # Shipping address
    full_name = serializers.CharField(max_length=200)
    phone = serializers.CharField(max_length=20)
    email = serializers.EmailField()
    street_address = serializers.CharField(max_length=500)
    city = serializers.CharField(max_length=100)
    state_province = serializers.CharField(max_length=100, required=False, default="")
    postal_code = serializers.CharField(max_length=20, required=False, default="")
    country = serializers.CharField(max_length=2, default="MN")
    notes = serializers.CharField(required=False, default="")
    payment_method = serializers.ChoiceField(choices=["qpay", "socialpay", "stripe"])
