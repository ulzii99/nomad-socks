from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("products.urls")),
    path("api/v1/", include("content.urls")),
    path("api/v1/accounts/", include("accounts.urls")),
    path("api/v1/", include("cart.urls")),
    path("api/v1/", include("orders.urls")),
    path("api/v1/", include("payments.urls")),
]
