from django.db import migrations
from django.utils.text import slugify


CATEGORIES = [
    {"name": "classic", "display_name_en": "Classic", "display_name_mn": "Сонгодог", "sort_order": 1},
    {"name": "patterned", "display_name_en": "Patterned", "display_name_mn": "Хээтэй", "sort_order": 2},
    {"name": "athletic", "display_name_en": "Athletic", "display_name_mn": "Спорт", "sort_order": 3},
]

PRODUCTS = [
    {
        "id": 1, "name_en": "Classic Black Everyday Socks",
        "name_mn": "Сонгодог хар өдөр тутмын оймс",
        "price": "8.99", "category": "classic",
        "description_en": "Timeless black cotton socks perfect for everyday wear. Soft, breathable, and durable.",
        "features": [
            "Premium cotton blend (80% cotton, 17% polyester, 3% elastane)",
            "Reinforced heel and toe",
            "Comfortable elastic band that stays up",
            "Machine washable",
        ],
        "featured": True,
    },
    {
        "id": 2, "name_en": "Classic White Everyday Socks",
        "name_mn": "Сонгодог цагаан өдөр тутмын оймс",
        "price": "8.99", "category": "classic",
        "description_en": "Clean white cotton socks for a fresh, classic look. Great for work or casual wear.",
        "features": [
            "Premium cotton blend (80% cotton, 17% polyester, 3% elastane)",
            "Reinforced heel and toe",
            "Comfortable elastic band that stays up",
            "Machine washable",
        ],
        "featured": True,
    },
    {
        "id": 3, "name_en": "Classic Gray Everyday Socks",
        "name_mn": "Сонгодог саарал өдөр тутмын оймс",
        "price": "8.99", "category": "classic",
        "description_en": "Versatile gray socks that go with everything. A wardrobe essential.",
        "features": [
            "Premium cotton blend (80% cotton, 17% polyester, 3% elastane)",
            "Reinforced heel and toe",
            "Comfortable elastic band that stays up",
            "Machine washable",
        ],
        "featured": False,
    },
    {
        "id": 4, "name_en": "Classic Navy Everyday Socks",
        "name_mn": "Сонгодог хар хөх өдөр тутмын оймс",
        "price": "8.99", "category": "classic",
        "description_en": "Deep navy blue socks perfect for professional settings or casual days.",
        "features": [
            "Premium cotton blend (80% cotton, 17% polyester, 3% elastane)",
            "Reinforced heel and toe",
            "Comfortable elastic band that stays up",
            "Machine washable",
        ],
        "featured": False,
    },
    {
        "id": 5, "name_en": "Nomad Stripe Pattern Socks",
        "name_mn": "Номад судалт хээтэй оймс",
        "price": "10.99", "category": "patterned",
        "description_en": "Bold stripes inspired by traditional Mongolian patterns. Stand out from the crowd.",
        "features": [
            "Premium cotton blend with enhanced durability",
            "Unique nomadic stripe design",
            "Reinforced heel and toe",
            "Machine washable",
        ],
        "featured": True,
    },
    {
        "id": 6, "name_en": "Steppe Earth Tone Socks",
        "name_mn": "Тал нутгийн газрын өнгөт оймс",
        "price": "10.99", "category": "patterned",
        "description_en": "Warm earth tones inspired by the Mongolian steppe. Subtle pattern for everyday style.",
        "features": [
            "Premium cotton blend with enhanced durability",
            "Earth-inspired color palette",
            "Reinforced heel and toe",
            "Machine washable",
        ],
        "featured": True,
    },
    {
        "id": 7, "name_en": "Geometric Pattern Socks",
        "name_mn": "Геометр хээтэй оймс",
        "price": "10.99", "category": "patterned",
        "description_en": "Modern geometric patterns meet traditional inspiration. Perfect for adding personality.",
        "features": [
            "Premium cotton blend with enhanced durability",
            "Contemporary geometric design",
            "Reinforced heel and toe",
            "Machine washable",
        ],
        "featured": False,
    },
    {
        "id": 8, "name_en": "Desert Sunset Socks",
        "name_mn": "Говийн нарны жаргалт оймс",
        "price": "10.99", "category": "patterned",
        "description_en": "Gradient colors inspired by Gobi Desert sunsets. A beautiful everyday statement.",
        "features": [
            "Premium cotton blend with enhanced durability",
            "Sunset-inspired gradient design",
            "Reinforced heel and toe",
            "Machine washable",
        ],
        "featured": False,
    },
    {
        "id": 9, "name_en": "Athletic Crew Socks",
        "name_mn": "Спорт crew оймс",
        "price": "9.99", "category": "athletic",
        "description_en": "Performance socks with extra cushioning for active days. Moisture-wicking and comfortable.",
        "features": [
            "Moisture-wicking fabric blend",
            "Extra cushioning in sole",
            "Arch support",
            "Reinforced heel and toe",
        ],
        "featured": False,
    },
    {
        "id": 10, "name_en": "Low-Cut Athletic Socks",
        "name_mn": "Богино спорт оймс",
        "price": "8.49", "category": "athletic",
        "description_en": "Sleek low-cut design perfect for sneakers and athletic shoes. Stays hidden while keeping feet comfortable.",
        "features": [
            "Low-cut design",
            "Moisture-wicking fabric blend",
            "Non-slip heel grip",
            "Lightweight and breathable",
        ],
        "featured": False,
    },
    {
        "id": 11, "name_en": "Classic Brown Everyday Socks",
        "name_mn": "Сонгодог хүрэн өдөр тутмын оймс",
        "price": "8.99", "category": "classic",
        "description_en": "Rich brown cotton socks with a natural, earthy tone. Perfect for autumn and casual style.",
        "features": [
            "Premium cotton blend (80% cotton, 17% polyester, 3% elastane)",
            "Reinforced heel and toe",
            "Comfortable elastic band that stays up",
            "Machine washable",
        ],
        "featured": False,
    },
    {
        "id": 12, "name_en": "Multi-Pack Classic Socks (5 pairs)",
        "name_mn": "Олон багц сонгодог оймс (5 хос)",
        "price": "34.99", "category": "classic",
        "description_en": "Value pack with 5 pairs of our classic everyday socks in assorted colors. Stock up and save!",
        "features": [
            "5 pairs included (Black, White, Gray, Navy, Brown)",
            "Premium cotton blend",
            "Reinforced heel and toe",
            "Machine washable",
        ],
        "featured": True,
    },
]


def seed_data(apps, schema_editor):
    Category = apps.get_model("products", "Category")
    Product = apps.get_model("products", "Product")
    ProductFeature = apps.get_model("products", "ProductFeature")
    ProductSize = apps.get_model("products", "ProductSize")

    # Create categories
    cat_map = {}
    for cat_data in CATEGORIES:
        cat = Category.objects.create(slug=cat_data["name"], **cat_data)
        cat_map[cat_data["name"]] = cat

    # Create products with features and sizes
    sizes = ["S", "M", "L"]
    for p in PRODUCTS:
        product = Product.objects.create(
            name_en=p["name_en"],
            name_mn=p["name_mn"],
            slug=slugify(p["name_en"]),
            price=p["price"],
            category=cat_map[p["category"]],
            description_en=p["description_en"],
            featured=p["featured"],
        )
        for i, feature_text in enumerate(p["features"]):
            ProductFeature.objects.create(
                product=product, text_en=feature_text, sort_order=i
            )
        for size in sizes:
            sku = f"NS-{product.pk:03d}-{size}"
            ProductSize.objects.create(product=product, size=size, sku=sku)


def reverse_seed(apps, schema_editor):
    Category = apps.get_model("products", "Category")
    Category.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_data, reverse_seed),
    ]
