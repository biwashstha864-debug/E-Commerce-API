from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema

from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


class CartView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
    summary="Get current user's cart",
    description=(
        "Returns the shopping cart belonging "
        "to the authenticated user."
    )
)
    def get(self, request):
        cart, created = Cart.objects.get_or_create(
            user=request.user
        )

        serializer = CartSerializer(cart)

        return Response(serializer.data)


class CartItemView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
    summary="Checkout cart",
    description=(
        "Creates an order from the authenticated "
        "user's cart and clears the cart."
    )
)
    def post(self, request):
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = serializer.validated_data["product"]
        quantity = serializer.validated_data["quantity"]

        cart, created = Cart.objects.get_or_create(
            user=request.user
        )

        if quantity > product.stock:
            return Response(
                {"detail": "Not enough stock."},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_item = CartItem.objects.filter(
            cart=cart,
            product=product
        ).first()

        if cart_item:
            new_quantity = cart_item.quantity + quantity

            if new_quantity > product.stock:
                return Response(
                    {"detail": "Not enough stock."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            cart_item.quantity = new_quantity
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=quantity
            )

        return Response(
            CartItemSerializer(cart_item).data,
            status=status.HTTP_201_CREATED
        )
    def patch(self, request, pk):
        cart = Cart.objects.get(user=request.user)

        cart_item = get_object_or_404(
            CartItem,
            id=pk,
            cart=cart
        )

        quantity = request.data.get("quantity")

        if quantity is None:
            return Response(
                {"quantity": "This field is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if quantity <= 0:
            return Response(
                {"quantity": "Quantity must be greater than zero."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if quantity > cart_item.product.stock:
            return Response(
                {"detail": "Not enough stock."},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_item.quantity = quantity
        cart_item.save()

        return Response(
            CartItemSerializer(cart_item).data
        )
        
    def delete(self, request, pk):
        cart = get_object_or_404(
            Cart,
            user=request.user
    )

        cart_item = get_object_or_404(
            CartItem,
            id=pk,
            cart=cart
    )

        cart_item.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
    )