from rest_framework import viewsets
from .serializers import ProductSerializer,CategorySerializer
from .models import Product,Category

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()   
    
    
