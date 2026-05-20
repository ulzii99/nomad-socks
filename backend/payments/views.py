from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from inventory.services import decrement_inventory_for_order
from orders.models import Order, OrderStatusHistory
from .models import Payment
from .providers import get_provider


def confirm_order_payment(order, provider_name, note=""):
    """Shared logic: confirm order and decrement inventory."""
    if order.status != "pending":
        return
    order.status = "confirmed"
    order.save()
    OrderStatusHistory.objects.create(
        order=order, status="confirmed",
        note=note or f"Payment received via {provider_name}",
    )
    decrement_inventory_for_order(order)


class CreatePaymentView(APIView):
    """Create a payment for an order using the specified provider."""

    def post(self, request):
        order_number = request.data.get("order_number")
        provider_name = request.data.get("payment_method")

        if not order_number or not provider_name:
            return Response(
                {"error": "order_number and payment_method are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            order = Order.objects.get(order_number=order_number)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if order.status not in ("pending",):
            return Response(
                {"error": "Order is not in a payable state."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create payment record
        payment = Payment.objects.create(
            order=order,
            provider=provider_name,
            amount=order.total,
            currency=order.currency,
            status="pending",
        )

        # Call provider to create invoice/intent
        provider = get_provider(provider_name)
        try:
            result = provider.create_invoice(order, payment)
        except Exception as e:
            payment.status = "failed"
            payment.save()
            return Response(
                {"error": f"Payment provider error: {str(e)}"},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        return Response({
            "payment_id": payment.id,
            "provider": provider_name,
            "order_number": order.order_number,
            "amount": str(payment.amount),
            "status": payment.status,
            **result,
        })


class CheckPaymentView(APIView):
    """Check the status of a payment."""

    def get(self, request, payment_id):
        try:
            payment = Payment.objects.get(pk=payment_id)
        except Payment.DoesNotExist:
            return Response(
                {"error": "Payment not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Check with provider
        provider = get_provider(payment.provider)
        new_status = provider.check_payment(payment)

        # If payment is now paid, confirm the order
        if new_status == "paid":
            confirm_order_payment(payment.order, payment.provider)

        return Response({
            "payment_id": payment.id,
            "status": payment.status,
            "order_number": payment.order.order_number,
            "order_status": payment.order.status,
        })


class QPayCallbackView(APIView):
    """QPay payment callback — called by QPay when payment is made."""

    def post(self, request):
        # QPay sends invoice_id in the callback
        invoice_id = request.data.get("invoice_id")
        if not invoice_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            payment = Payment.objects.get(
                provider="qpay", provider_invoice_id=invoice_id
            )
        except Payment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Verify with QPay
        provider = get_provider("qpay")
        new_status = provider.check_payment(payment)

        if new_status == "paid":
            confirm_order_payment(payment.order, "qpay", "Payment confirmed via QPay callback")

        return Response({"status": "ok"})


class SocialPayCallbackView(APIView):
    """SocialPay payment callback."""

    def post(self, request):
        invoice_id = request.data.get("invoice_id")
        if not invoice_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            payment = Payment.objects.get(
                provider="socialpay", provider_invoice_id=invoice_id
            )
        except Payment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        provider = get_provider("socialpay")
        new_status = provider.check_payment(payment)

        if new_status == "paid":
            confirm_order_payment(payment.order, "socialpay", "Payment confirmed via SocialPay callback")

        return Response({"status": "ok"})
