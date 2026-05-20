from django.conf import settings
from django.db import models


class InventoryRecord(models.Model):
    product_size = models.OneToOneField(
        "products.ProductSize", on_delete=models.CASCADE, related_name="inventory"
    )
    quantity_on_hand = models.PositiveIntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(default=10)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product_size} - {self.quantity_on_hand} in stock"

    @property
    def is_low_stock(self):
        return self.quantity_on_hand <= self.low_stock_threshold

    @property
    def is_out_of_stock(self):
        return self.quantity_on_hand == 0


class Machine(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("maintenance", "Maintenance"),
        ("inactive", "Inactive"),
    ]

    name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.status})"


class ProductionRun(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.PROTECT, related_name="production_runs")
    product_size = models.ForeignKey(
        "products.ProductSize", on_delete=models.PROTECT, related_name="production_runs"
    )
    quantity_produced = models.PositiveIntegerField()
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-started_at"]

    def __str__(self):
        return f"{self.machine.name} - {self.product_size} - {self.quantity_produced} units"


class InventoryAdjustment(models.Model):
    TYPE_CHOICES = [
        ("production", "Production"),
        ("sale", "Sale"),
        ("return", "Return"),
        ("damage", "Damage"),
        ("manual", "Manual Adjustment"),
    ]

    product_size = models.ForeignKey(
        "products.ProductSize", on_delete=models.CASCADE, related_name="adjustments"
    )
    adjustment_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    quantity_change = models.IntegerField(help_text="Positive = increase, negative = decrease")
    reference = models.CharField(max_length=200, blank=True, help_text="Order number, production run ID, etc.")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        sign = "+" if self.quantity_change > 0 else ""
        return f"{self.product_size} {sign}{self.quantity_change} ({self.adjustment_type})"
