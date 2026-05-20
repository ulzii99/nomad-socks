"""Inventory business logic."""

import logging

from products.models import ProductSize
from .models import InventoryAdjustment, InventoryRecord

logger = logging.getLogger(__name__)


def decrement_inventory_for_order(order):
    """Reduce inventory for each item in a confirmed order."""
    for item in order.items.all():
        try:
            product_size = ProductSize.objects.get(
                product=item.product, size=item.size
            )
        except ProductSize.DoesNotExist:
            logger.warning(
                f"ProductSize not found for {item.product.name_en} size {item.size}"
            )
            continue

        record, _ = InventoryRecord.objects.get_or_create(
            product_size=product_size,
            defaults={"quantity_on_hand": 0},
        )

        new_qty = max(0, record.quantity_on_hand - item.quantity)
        record.quantity_on_hand = new_qty
        record.save()

        InventoryAdjustment.objects.create(
            product_size=product_size,
            adjustment_type="sale",
            quantity_change=-item.quantity,
            reference=order.order_number,
        )

        if record.is_low_stock:
            logger.warning(
                f"LOW STOCK: {product_size} has {record.quantity_on_hand} units "
                f"(threshold: {record.low_stock_threshold})"
            )
