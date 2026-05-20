from django.db import migrations


def seed_shipping(apps, schema_editor):
    ShippingZone = apps.get_model("shipping", "ShippingZone")
    ShippingRate = apps.get_model("shipping", "ShippingRate")

    # Mongolia domestic
    mn = ShippingZone.objects.create(
        name="Mongolia Domestic",
        name_mn="Дотоод хүргэлт",
        countries=["MN"],
        sort_order=1,
    )
    ShippingRate.objects.create(
        zone=mn, name="Standard", name_mn="Энгийн",
        price=5000, free_shipping_threshold=50000,
        estimated_days_min=3, estimated_days_max=5,
    )
    ShippingRate.objects.create(
        zone=mn, name="Express", name_mn="Шуурхай",
        price=10000, free_shipping_threshold=0,
        estimated_days_min=1, estimated_days_max=2,
    )

    # Asia
    asia = ShippingZone.objects.create(
        name="Asia",
        name_mn="Ази",
        countries=["CN", "KR", "JP", "TW", "HK", "SG", "TH", "VN", "MY", "ID", "PH", "IN"],
        sort_order=2,
    )
    ShippingRate.objects.create(
        zone=asia, name="Standard", name_mn="Энгийн",
        price=15000, free_shipping_threshold=0,
        estimated_days_min=7, estimated_days_max=12,
    )

    # International
    intl = ShippingZone.objects.create(
        name="International",
        name_mn="Олон улсын",
        countries=["US", "CA", "GB", "DE", "FR", "AU", "NZ"],
        sort_order=3,
    )
    ShippingRate.objects.create(
        zone=intl, name="Standard", name_mn="Энгийн",
        price=25000, free_shipping_threshold=0,
        estimated_days_min=10, estimated_days_max=20,
    )


def reverse(apps, schema_editor):
    ShippingZone = apps.get_model("shipping", "ShippingZone")
    ShippingZone.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("shipping", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_shipping, reverse),
    ]
