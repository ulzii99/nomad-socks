from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Category, Product
from .serializers import (
    CategorySerializer,
    ProductDetailSerializer,
    ProductListSerializer,
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True).select_related("category")
    lookup_field = "slug"
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category__name", "featured"]
    search_fields = ["name_en", "name_mn", "description_en"]
    ordering_fields = ["price", "name_en", "created_at"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProductDetailSerializer
        return ProductListSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == "retrieve":
            qs = qs.prefetch_related("features", "images", "sizes")
        return qs

    @action(detail=False, url_path="featured")
    def featured(self, request):
        featured = self.get_queryset().filter(featured=True)
        serializer = ProductListSerializer(featured, many=True)
        return Response(serializer.data)

    @action(detail=True, url_path="related")
    def related(self, request, slug=None):
        product = self.get_object()
        related = (
            self.get_queryset()
            .filter(category=product.category)
            .exclude(pk=product.pk)[:4]
        )
        serializer = ProductListSerializer(related, many=True)
        return Response(serializer.data)
