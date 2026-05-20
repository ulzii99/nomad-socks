from django.urls import path

from . import views

urlpatterns = [
    path("admin/dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("admin/analytics/top-products/", views.TopProductsView.as_view(), name="top-products"),
    path("admin/analytics/revenue/", views.RevenueReportView.as_view(), name="revenue-report"),
]
