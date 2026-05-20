from django.urls import path

from . import views

urlpatterns = [
    path("shipping/rates/", views.ShippingRatesView.as_view(), name="shipping-rates"),
]
