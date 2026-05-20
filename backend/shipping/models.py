from django.db import models


class ShippingZone(models.Model):
    name = models.CharField(max_length=100)
    name_mn = models.CharField(max_length=100, blank=True)
    countries = models.JSONField(default=list, help_text="ISO 3166-1 alpha-2 country codes")
    is_active = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]

    def __str__(self):
        return self.name


class ShippingRate(models.Model):
    zone = models.ForeignKey(ShippingZone, on_delete=models.CASCADE, related_name="rates")
    name = models.CharField(max_length=100)
    name_mn = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    free_shipping_threshold = models.DecimalField(
        max_digits=8, decimal_places=2, default=0,
        help_text="Order subtotal above which shipping is free. 0 = never free.",
    )
    estimated_days_min = models.PositiveIntegerField()
    estimated_days_max = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["price"]

    def __str__(self):
        return f"{self.zone.name} - {self.name} ({self.price})"

    def get_price_for_subtotal(self, subtotal):
        """Returns 0 if subtotal exceeds free shipping threshold."""
        if self.free_shipping_threshold and subtotal >= self.free_shipping_threshold:
            return 0
        return self.price


class Shipment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("picked_up", "Picked Up"),
        ("in_transit", "In Transit"),
        ("delivered", "Delivered"),
        ("returned", "Returned"),
    ]

    order = models.ForeignKey(
        "orders.Order", on_delete=models.CASCADE, related_name="shipments"
    )
    tracking_number = models.CharField(max_length=200, blank=True)
    carrier = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    shipping_rate = models.ForeignKey(
        ShippingRate, on_delete=models.SET_NULL, null=True, blank=True
    )
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Shipment for {self.order.order_number} - {self.status}"
