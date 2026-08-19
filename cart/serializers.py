from rest_framework import serializers
from .models import CartItem,Cart
from products.models import Product

class ProductReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "name",
        ]
        
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductReadSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "quantity",
        ]

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many = True,read_only = True)
    
    class Meta:
        model = Cart
        fields = [
            "id",
            "items",
            "created_at",
            "updated_at",
        ]

    