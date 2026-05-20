from rest_framework import serializers

from .models import ShippingRate, ShippingZone


class ShippingRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingRate
        fields = [
            "id", "name", "name_mn", "price",
            "free_shipping_threshold", "estimated_days_min", "estimated_days_max",
        ]


class ShippingZoneSerializer(serializers.ModelSerializer):
    rates = ShippingRateSerializer(many=True, read_only=True)

    class Meta:
        model = ShippingZone
        fields = ["id", "name", "name_mn", "countries", "rates"]
