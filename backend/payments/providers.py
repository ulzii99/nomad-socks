"""
Payment provider integrations for QPay, SocialPay, and Stripe.

Each provider implements:
  - create_invoice(order, payment) -> dict with provider-specific data
  - check_payment(payment) -> updated status string

NOTE: QPay and SocialPay require API credentials from the providers.
Set these in environment variables:
  - QPAY_USERNAME, QPAY_PASSWORD, QPAY_INVOICE_CODE
  - SOCIALPAY_APP_ID, SOCIALPAY_SECRET
  - STRIPE_SECRET_KEY
"""

import logging

from django.conf import settings

logger = logging.getLogger(__name__)


class QPayProvider:
    """
    QPay integration via developer.qpay.mn API.

    Flow:
    1. Authenticate to get access token
    2. Create invoice -> returns QR code URLs
    3. Customer scans QR with bank app and pays
    4. Check payment status via API or receive callback
    """
    BASE_URL = "https://merchant.qpay.mn/v2"

    def __init__(self):
        self.username = getattr(settings, "QPAY_USERNAME", "")
        self.password = getattr(settings, "QPAY_PASSWORD", "")
        self.invoice_code = getattr(settings, "QPAY_INVOICE_CODE", "")

    def _get_token(self):
        """Get access token from QPay. In production, cache this token."""
        import requests
        response = requests.post(
            f"{self.BASE_URL}/auth/token",
            auth=(self.username, self.password),
        )
        response.raise_for_status()
        return response.json()["access_token"]

    def create_invoice(self, order, payment):
        """Create a QPay invoice and return QR data."""
        if not self.username:
            # Dev mode: return mock data
            logger.warning("QPay credentials not configured, using mock response")
            return {
                "invoice_id": f"mock-qpay-{order.order_number}",
                "qr_code_url": "",
                "qr_text": "mock-qr-data",
                "urls": [],
            }

        import requests
        token = self._get_token()
        response = requests.post(
            f"{self.BASE_URL}/invoice",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "invoice_code": self.invoice_code,
                "sender_invoice_no": order.order_number,
                "invoice_receiver_code": order.guest_phone or "terminal",
                "invoice_description": f"Nomad Socks Order {order.order_number}",
                "amount": float(order.total),
                "callback_url": f"{settings.BACKEND_URL}/api/v1/payments/qpay/callback/",
            },
        )
        response.raise_for_status()
        data = response.json()

        payment.provider_invoice_id = data.get("invoice_id", "")
        payment.qr_code_url = data.get("qr_image", "")
        payment.provider_response = data
        payment.save()

        return data

    def check_payment(self, payment):
        """Check if QPay invoice has been paid."""
        if not self.username or not payment.provider_invoice_id:
            return payment.status

        import requests
        token = self._get_token()
        response = requests.post(
            f"{self.BASE_URL}/payment/check",
            headers={"Authorization": f"Bearer {token}"},
            json={"object_type": "INVOICE", "object_id": payment.provider_invoice_id},
        )
        response.raise_for_status()
        data = response.json()

        if data.get("count", 0) > 0:
            payment.status = "paid"
            payment.provider_payment_id = str(data["rows"][0].get("payment_id", ""))
            payment.provider_response = data
            payment.save()
            return "paid"

        return "pending"


class SocialPayProvider:
    """
    SocialPay integration via Golomt Bank API.

    Flow:
    1. Create checkout request with basket
    2. Returns payment URL / QR
    3. Customer pays via SocialPay app
    4. Receive callback or check status
    """
    BASE_URL = "https://ecommerce.golomtbank.com/api"

    def __init__(self):
        self.app_id = getattr(settings, "SOCIALPAY_APP_ID", "")
        self.secret = getattr(settings, "SOCIALPAY_SECRET", "")

    def create_invoice(self, order, payment):
        """Create a SocialPay checkout."""
        if not self.app_id:
            logger.warning("SocialPay credentials not configured, using mock response")
            return {
                "invoice_id": f"mock-socialpay-{order.order_number}",
                "checkout_url": "",
            }

        import requests
        response = requests.post(
            f"{self.BASE_URL}/invoice",
            headers={"Authorization": f"Bearer {self.secret}"},
            json={
                "amount": float(order.total),
                "description": f"Nomad Socks Order {order.order_number}",
                "callback_url": f"{settings.BACKEND_URL}/api/v1/payments/socialpay/callback/",
                "return_url": f"{settings.FRONTEND_URL}/order-confirmation.html?order={order.order_number}",
            },
        )
        response.raise_for_status()
        data = response.json()

        payment.provider_invoice_id = data.get("invoice_id", "")
        payment.provider_response = data
        payment.save()

        return data

    def check_payment(self, payment):
        """Check SocialPay payment status."""
        if not self.app_id or not payment.provider_invoice_id:
            return payment.status
        # TODO: implement actual status check
        return payment.status


class StripeProvider:
    """
    Stripe integration for international payments.

    Flow:
    1. Create PaymentIntent server-side
    2. Return client_secret to frontend
    3. Frontend confirms payment with Stripe.js
    4. Webhook confirms payment
    """

    def __init__(self):
        self.secret_key = getattr(settings, "STRIPE_SECRET_KEY", "")

    def create_invoice(self, order, payment):
        """Create a Stripe PaymentIntent."""
        if not self.secret_key:
            logger.warning("Stripe credentials not configured, using mock response")
            return {
                "client_secret": "mock_secret",
                "payment_intent_id": f"mock-pi-{order.order_number}",
            }

        import stripe
        stripe.api_key = self.secret_key

        intent = stripe.PaymentIntent.create(
            amount=int(order.total * 100),  # Stripe uses cents
            currency="usd",
            metadata={"order_number": order.order_number},
        )

        payment.provider_invoice_id = intent.id
        payment.provider_response = {"id": intent.id}
        payment.save()

        return {"client_secret": intent.client_secret, "payment_intent_id": intent.id}

    def check_payment(self, payment):
        """Check Stripe PaymentIntent status."""
        if not self.secret_key or not payment.provider_invoice_id:
            return payment.status

        import stripe
        stripe.api_key = self.secret_key
        intent = stripe.PaymentIntent.retrieve(payment.provider_invoice_id)
        if intent.status == "succeeded":
            payment.status = "paid"
            payment.save()
            return "paid"
        return payment.status


def get_provider(provider_name):
    """Factory function to get payment provider."""
    providers = {
        "qpay": QPayProvider,
        "socialpay": SocialPayProvider,
        "stripe": StripeProvider,
    }
    provider_class = providers.get(provider_name)
    if not provider_class:
        raise ValueError(f"Unknown payment provider: {provider_name}")
    return provider_class()
