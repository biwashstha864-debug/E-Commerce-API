from django.urls import path
from .views import CartView,CartItem

urlpatterns = [
   path( "",CartView.as_view(),name= "cart"),
   path("items/",CartItem.as_view(),name = "cart-items"),
   path("items/<int:pk>/",CartItem.as_view())
]
