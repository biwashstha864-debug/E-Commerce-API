from django.db import transaction
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdmin
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema

from cart.models import Cart
from .models import Order, OrderItem
from .serializers import OrderSerializer


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        summary="Checkout cart",
        description=(
            "Creates an order from the authenticated "
            "user's cart and clears the cart."
        )
)
    @transaction.atomic
    def post(self, request):

        cart = Cart.objects.get(
            user=request.user
        )

        cart_items = cart.items.select_related(
            "product"
        )

        if not cart_items.exists():
            return Response(
                {"detail": "Cart is empty."},
                status=status.HTTP_400_BAD_REQUEST
            )

        for item in cart_items:
            if item.quantity > item.product.stock:
                return Response(
                    {
                        "detail": (
                            f"Not enough stock for "
                            f"{item.product.name}."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        order = Order.objects.create(
            user=request.user
        )

        total = 0

        for item in cart_items:

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

            total += item.product.price * item.quantity

            item.product.stock -= item.quantity
            item.product.save(
                update_fields=["stock"]
            )

        order.total_price = total
        order.save(
            update_fields=["total_price"]
        )

        cart.items.all().delete()

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED
        )
        

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(
            user=self.request.user
        )
        
    @action(
        detail=True,
        methods=["patch"],
        permission_classes=[IsAdmin]
    )
    def update_status(self, request, pk=None):
        order = self.get_object()

        new_status = request.data.get("status")

        if new_status not in Order.Status.values:
            return Response(
                {"detail": "Invalid status."},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = new_status
        order.save(update_fields=["status"])

        return Response(
            OrderSerializer(order).data
        )
        
    @action(
        detail=True,
        methods=["post"]
    )
    def cancel(self, request, pk=None):
        order = self.get_object()

        if order.status in [
            Order.Status.SHIPPED,
            Order.Status.DELIVERED,
            Order.Status.CANCELED,
        ]:
            return Response(
                {"detail": "This order cannot be cancelled."},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.status = Order.Status.CANCELED
        order.save(update_fields=["status"])

        return Response(
            OrderSerializer(order).data
        )