from rest_framework import serializers
from .models import Category,Product,ProductImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields  ="__all__"
        

class ProductWriteSerializer(serializers.ModelSerializer):
    class Meta :
        model = Product
        fields = [
            "name",
            "description",
            "price",
            "stock",
            "category",
        ]
        


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = [
            "id",
            "image",
            "created_at",
        ]
        
class ProductReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only = True)
    images = ProductImageSerializer(many = True,read_only = True)
    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "price",
            "images",
            "stock",
            "category",
            "created_at",
            "updated_at",
    ]
            
