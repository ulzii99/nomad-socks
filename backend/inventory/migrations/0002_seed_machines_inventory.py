from django.db import migrations


def seed_machines_and_inventory(apps, schema_editor):
    Machine = apps.get_model("inventory", "Machine")
    InventoryRecord = apps.get_model("inventory", "InventoryRecord")
    ProductSize = apps.get_model("products", "ProductSize")

    # Create 4 machines
    for i in range(1, 5):
        Machine.objects.create(name=f"Machine {i}", status="active")

    # Create inventory records for all product sizes with initial stock
    for ps in ProductSize.objects.all():
        InventoryRecord.objects.create(
            product_size=ps,
            quantity_on_hand=50,
            low_stock_threshold=10,
        )


def reverse(apps, schema_editor):
    Machine = apps.get_model("inventory", "Machine")
    InventoryRecord = apps.get_model("inventory", "InventoryRecord")
    Machine.objects.all().delete()
    InventoryRecord.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0001_initial"),
        ("products", "0002_seed_products"),
    ]

    operations = [
        migrations.RunPython(seed_machines_and_inventory, reverse),
    ]
