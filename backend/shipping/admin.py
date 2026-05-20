from django.contrib import admin

from .models import Shipment, ShippingRate, ShippingZone


class ShippingRateInline(admin.TabularInline):
    model = ShippingRate
    extra = 1


@admin.register(ShippingZone)
class ShippingZoneAdmin(admin.ModelAdmin):
    list_display = ("name", "countries", "is_active", "sort_order")
    inlines = [ShippingRateInline]


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ("order", "carrier", "tracking_number", "status", "shipped_at")
    list_filter = ("status", "carrier")
    search_fields = ("order__order_number", "tracking_number")
