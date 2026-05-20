from django.contrib import admin

from .models import Order, OrderItem, OrderStatusHistory


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "product_name", "size", "quantity", "unit_price", "total_price")


class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ("status", "note", "created_at", "created_by")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "customer_display", "status", "total", "currency", "created_at")
    list_filter = ("status", "currency", "created_at")
    search_fields = ("order_number", "guest_email", "guest_name", "user__username")
    readonly_fields = ("order_number", "created_at", "updated_at")
    inlines = [OrderItemInline, OrderStatusHistoryInline]

    def customer_display(self, obj):
        if obj.user:
            return obj.user.username
        return obj.guest_name or obj.guest_email
    customer_display.short_description = "Customer"
