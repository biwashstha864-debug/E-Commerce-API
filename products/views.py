from rest_framework import viewsets
from .serializers import CategorySerializer,ProductReadSerializer,ProductWriteSerializer
from .models import Product,Category
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from .filters import ProductFilter

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()   
    
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("category").all()

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


    
    
    
