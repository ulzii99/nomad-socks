from django.urls import path

from . import views

urlpatterns = [
    path("cart/", views.CartView.as_view(), name="cart"),
    path("cart/items/", views.CartItemView.as_view(), name="cart-items"),
    path("cart/items/<int:item_id>/", views.CartItemDetailView.as_view(), name="cart-item-detail"),
    path("cart/clear/", views.CartClearView.as_view(), name="cart-clear"),
    path("cart/merge/", views.CartMergeView.as_view(), name="cart-merge"),
]
