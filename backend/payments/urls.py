from django.urls import path

from . import views

urlpatterns = [
    path("payments/create/", views.CreatePaymentView.as_view(), name="payment-create"),
    path("payments/<int:payment_id>/check/", views.CheckPaymentView.as_view(), name="payment-check"),
    path("payments/qpay/callback/", views.QPayCallbackView.as_view(), name="qpay-callback"),
    path("payments/socialpay/callback/", views.SocialPayCallbackView.as_view(), name="socialpay-callback"),
]
