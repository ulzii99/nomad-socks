from rest_framework import serializers

from .models import Category, Product, ProductFeature, ProductImage, ProductSize


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "display_name_en", "display_name_mn", "slug"]


class ProductFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFeature
        fields = ["id", "text_en", "text_mn"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "alt_text", "is_primary"]


class ProductSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSize
        fields = ["id", "size", "sku"]


class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for product listings."""
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "name_en", "name_mn", "slug", "price",
            "category", "featured",
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    """Full serializer with features, images, and sizes."""
    category = CategorySerializer(read_only=True)
    features = ProductFeatureSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    sizes = ProductSizeSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "name_en", "name_mn", "slug", "price",
            "category", "description_en", "description_mn",
            "featured", "features", "images", "sizes",
        ]
