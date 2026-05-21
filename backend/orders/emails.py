"""Email notifications for orders."""

import logging

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def send_order_confirmation(order):
    """Send order confirmation email to customer."""
    email = order.guest_email or (order.user.email if order.user else None)
    if not email:
        logger.warning(f"No email for order {order.order_number}, skipping notification")
        return

    lang = order.language or "mn"
    subject = {
        "mn": f"Захиалга баталгаажлаа - {order.order_number}",
        "en": f"Order Confirmed - {order.order_number}",
    }.get(lang, f"Order Confirmed - {order.order_number}")

    context = {
        "order": order,
        "items": order.items.all(),
        "lang": lang,
    }

    try:
        html_message = render_to_string("orders/email_confirmation.html", context)
        plain_message = _build_plain_confirmation(order, lang)

        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            html_message=html_message,
            fail_silently=True,
        )
        logger.info(f"Order confirmation sent to {email} for {order.order_number}")
    except Exception as e:
        logger.error(f"Failed to send confirmation for {order.order_number}: {e}")


def send_order_status_update(order, new_status, note=""):
    """Send status update email to customer."""
    email = order.guest_email or (order.user.email if order.user else None)
    if not email:
        return

    lang = order.language or "mn"

    status_labels = {
        "mn": {
            "confirmed": "Баталгаажсан",
            "processing": "Боловсруулж байна",
            "shipped": "Илгээсэн",
            "delivered": "Хүргэгдсэн",
            "cancelled": "Цуцлагдсан",
            "refunded": "Буцаагдсан",
        },
        "en": {
            "confirmed": "Confirmed",
            "processing": "Processing",
            "shipped": "Shipped",
            "delivered": "Delivered",
            "cancelled": "Cancelled",
            "refunded": "Refunded",
        },
    }

    status_label = status_labels.get(lang, status_labels["en"]).get(new_status, new_status)

    subject = {
        "mn": f"Захиалгын төлөв шинэчлэгдлээ - {order.order_number}",
        "en": f"Order Status Update - {order.order_number}",
    }.get(lang, f"Order Status Update - {order.order_number}")

    if lang == "mn":
        message = (
            f"Сайн байна уу,\n\n"
            f"Таны захиалга {order.order_number} төлөв шинэчлэгдлээ: {status_label}\n"
        )
        if note:
            message += f"\nТэмдэглэл: {note}\n"
        message += f"\nБаярлалаа,\nНомад Сокс"
    else:
        message = (
            f"Hello,\n\n"
            f"Your order {order.order_number} has been updated to: {status_label}\n"
        )
        if note:
            message += f"\nNote: {note}\n"
        message += f"\nThank you,\nNomad Socks"

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=True,
        )
        logger.info(f"Status update sent to {email} for {order.order_number}")
    except Exception as e:
        logger.error(f"Failed to send status update for {order.order_number}: {e}")


def _build_plain_confirmation(order, lang):
    """Plain text fallback for order confirmation."""
    items_text = "\n".join(
        f"  - {item.product_name} ({item.size}) x{item.quantity} = ${item.total_price}"
        for item in order.items.all()
    )

    if lang == "mn":
        return (
            f"Сайн байна уу,\n\n"
            f"Таны захиалга амжилттай бүртгэгдлээ.\n\n"
            f"Захиалгын дугаар: {order.order_number}\n"
            f"Бараа:\n{items_text}\n\n"
            f"Нийт: ${order.total}\n\n"
            f"Баярлалаа,\nНомад Сокс"
        )
    return (
        f"Hello,\n\n"
        f"Your order has been placed successfully.\n\n"
        f"Order Number: {order.order_number}\n"
        f"Items:\n{items_text}\n\n"
        f"Total: ${order.total}\n\n"
        f"Thank you,\nNomad Socks"
    )
