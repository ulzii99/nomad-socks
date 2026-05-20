from django.contrib import admin

from .models import Category, Product, ProductFeature, ProductImage, ProductSize


class ProductFeatureInline(admin.TabularInline):
    model = ProductFeature
    extra = 1


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "display_name_en", "display_name_mn", "sort_order")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name_en", "category", "price", "featured", "is_active")
    list_filter = ("category", "featured", "is_active")
    search_fields = ("name_en", "name_mn")
    prepopulated_fields = {"slug": ("name_en",)}
    inlines = [ProductFeatureInline, ProductImageInline, ProductSizeInline]
