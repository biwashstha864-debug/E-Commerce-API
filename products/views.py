from rest_framework import viewsets
from .serializers import CategorySerializer,ProductReadSerializer,ProductWriteSerializer,ProductImageSerializer
from .models import Product,Category,ProductImage
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from .filters import ProductFilter
from rest_framework.parsers import MultiPartParser,FormParser
from django.shortcuts import get_object_or_404

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()   
    
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("category").prefetch_related(
        "images"
    )

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    filterset_class= ProductFilter
    search_fields = ["name"]
    ordering_fields = [
        "price",
        "stock",
        "created_at",
        "name"
    ]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ProductReadSerializer

        return ProductWriteSerializer

class ProductImageViewSet(viewsets.ModelViewSet):
    serializer_class = ProductImageSerializer
    parser_classes = [MultiPartParser,FormParser]
    
    def perform_create(self, serializer):
        product_id = self.kwargs["product_id"]
        product  = get_object_or_404(Product,id = product_id)
        
        serializer.save(product=product)
        
    def get_queryset(self):
        product_id = self.kwargs["product_id"]
        return ProductImage.objects.filter(product_id = product_id) 
    
