from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet,ProductViewSet
from django.urls import path
from .views import ProductImageViewSet

router = DefaultRouter()

router.register(
    "categories",
    CategoryViewSet 
)
router.register(
    "products",
    ProductViewSet
)
urlpatterns = router.urls

urlpatterns += [
    path(
        "products/<int:product_id>/images/",
        ProductImageViewSet.as_view({
            "get": "list",
            "post": "create",
        }),
    ),
]
