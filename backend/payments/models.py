from django.db import models


class Payment(models.Model):
    PROVIDER_CHOICES = [
        ("qpay", "QPay"),
        ("socialpay", "SocialPay"),
        ("stripe", "Stripe"),
    ]
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
        ("cancelled", "Cancelled"),
    ]

    order = models.ForeignKey(
        "orders.Order", on_delete=models.CASCADE, related_name="payments"
    )
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES)
    provider_invoice_id = models.CharField(max_length=200, blank=True)
    provider_payment_id = models.CharField(max_length=200, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="MNT")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    qr_code_url = models.URLField(blank=True)
    provider_response = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.provider} - {self.order.order_number} - {self.status}"
