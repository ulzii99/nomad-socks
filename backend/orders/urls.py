from django.urls import path

from . import views

urlpatterns = [
    path("orders/checkout/", views.CheckoutView.as_view(), name="checkout"),
    path("orders/", views.OrderListView.as_view(), name="order-list"),
    path("orders/<str:order_number>/", views.OrderDetailView.as_view(), name="order-detail"),
    path("admin/orders/", views.AdminOrderListView.as_view(), name="admin-order-list"),
    path("admin/orders/<str:order_number>/status/", views.AdminOrderStatusUpdateView.as_view(), name="admin-order-status"),
]
