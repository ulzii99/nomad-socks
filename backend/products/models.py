from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    display_name_en = models.CharField(max_length=100)
    display_name_mn = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    sort_order = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.display_name_en


class Product(models.Model):
    name_en = models.CharField(max_length=200)
    name_mn = models.CharField(max_length=200, blank=True)
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="products"
    )
    description_en = models.TextField()
    description_mn = models.TextField(blank=True)
    featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-featured", "name_en"]

    def __str__(self):
        return self.name_en


class ProductFeature(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="features"
    )
    text_en = models.CharField(max_length=300)
    text_mn = models.CharField(max_length=300, blank=True)
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]

    def __str__(self):
        return self.text_en[:50]


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="products/")
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ["-is_primary", "sort_order"]

    def __str__(self):
        return f"{self.product.name_en} - image {self.pk}"


class ProductSize(models.Model):
    SIZE_CHOICES = [
        ("S", "Small (US 5-7)"),
        ("M", "Medium (US 8-10)"),
        ("L", "Large (US 11-13)"),
    ]
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="sizes"
    )
    size = models.CharField(max_length=2, choices=SIZE_CHOICES)
    sku = models.CharField(max_length=50, unique=True)

    class Meta:
        unique_together = ("product", "size")

    def __str__(self):
        return f"{self.product.name_en} - {self.size}"
