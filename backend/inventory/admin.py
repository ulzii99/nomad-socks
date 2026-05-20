from django.contrib import admin

from .models import InventoryAdjustment, InventoryRecord, Machine, ProductionRun


@admin.register(InventoryRecord)
class InventoryRecordAdmin(admin.ModelAdmin):
    list_display = ("product_size", "quantity_on_hand", "low_stock_threshold", "is_low_stock", "updated_at")
    list_filter = ("product_size__size",)
    search_fields = ("product_size__product__name_en",)

    def is_low_stock(self, obj):
        return obj.is_low_stock
    is_low_stock.boolean = True


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "created_at")
    list_filter = ("status",)


@admin.register(ProductionRun)
class ProductionRunAdmin(admin.ModelAdmin):
    list_display = ("machine", "product_size", "quantity_produced", "started_at", "completed_at")
    list_filter = ("machine", "completed_at")
    search_fields = ("product_size__product__name_en",)


@admin.register(InventoryAdjustment)
class InventoryAdjustmentAdmin(admin.ModelAdmin):
    list_display = ("product_size", "adjustment_type", "quantity_change", "reference", "created_at")
    list_filter = ("adjustment_type",)
    search_fields = ("product_size__product__name_en", "reference")
    readonly_fields = ("created_at",)
