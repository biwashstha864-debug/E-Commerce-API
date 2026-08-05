from rest_framework import serializers
from .models import Category,Product

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
        
class ProductReadSerializer(serializers.ModelSerializer):
    
    category = CategorySerializer(read_only = True)
     
    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "price",
            "stock",
            "category",
            "created_at",
            "updated_at",
    ]
        
