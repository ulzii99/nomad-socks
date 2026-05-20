from django.urls import path

from . import views

urlpatterns = [
    path("admin/inventory/", views.InventoryOverviewView.as_view(), name="inventory-overview"),
    path("admin/inventory/adjust/", views.InventoryAdjustView.as_view(), name="inventory-adjust"),
    path("admin/machines/", views.MachineListView.as_view(), name="machine-list"),
]
