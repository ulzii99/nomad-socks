from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product
from .models import Cart, CartItem
from .serializers import (
    CartItemCreateSerializer,
    CartItemUpdateSerializer,
    CartSerializer,
)


def get_or_create_cart(request):
    """Get or create a cart for the current user or session."""
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart

    # Guest cart via session
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    cart, _ = Cart.objects.get_or_create(session_key=session_key)
    return cart


class CartView(APIView):
    def get(self, request):
        cart = get_or_create_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class CartItemView(APIView):
    def post(self, request):
        """Add item to cart."""
        serializer = CartItemCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = get_or_create_cart(request)
        product_id = serializer.validated_data["product_id"]
        size = serializer.validated_data["size"]
        quantity = serializer.validated_data["quantity"]

        try:
            product = Product.objects.get(pk=product_id, is_active=True)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        item, created = CartItem.objects.get_or_create(
            cart=cart, product=product, size=size,
            defaults={"quantity": quantity},
        )
        if not created:
            item.quantity += quantity
            item.save()

        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)


class CartItemDetailView(APIView):
    def patch(self, request, item_id):
        """Update item quantity."""
        serializer = CartItemUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = get_or_create_cart(request)
        try:
            item = CartItem.objects.get(pk=item_id, cart=cart)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)

        item.quantity = serializer.validated_data["quantity"]
        item.save()
        return Response(CartSerializer(cart).data)

    def delete(self, request, item_id):
        """Remove item from cart."""
        cart = get_or_create_cart(request)
        try:
            item = CartItem.objects.get(pk=item_id, cart=cart)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)

        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartClearView(APIView):
    def delete(self, request):
        """Clear all items from cart."""
        cart = get_or_create_cart(request)
        cart.items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartMergeView(APIView):
    def post(self, request):
        """Merge guest cart items (from localStorage) into the user's cart on login."""
        if not request.user.is_authenticated:
            return Response(
                {"error": "Authentication required."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        items = request.data.get("items", [])
        cart, _ = Cart.objects.get_or_create(user=request.user)

        for item_data in items:
            product_id = item_data.get("productId") or item_data.get("product_id")
            size = item_data.get("size", "M")
            quantity = item_data.get("quantity", 1)

            try:
                product = Product.objects.get(pk=product_id, is_active=True)
            except Product.DoesNotExist:
                continue

            item, created = CartItem.objects.get_or_create(
                cart=cart, product=product, size=size,
                defaults={"quantity": quantity},
            )
            if not created:
                item.quantity = max(item.quantity, quantity)
                item.save()

        # Clean up guest cart if session exists
        session_key = request.session.session_key
        if session_key:
            Cart.objects.filter(session_key=session_key).exclude(pk=cart.pk).delete()

        return Response(CartSerializer(cart).data)
