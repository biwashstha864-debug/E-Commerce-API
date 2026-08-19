from django.urls import path
from .views import CartView,CartItemView

urlpatterns = [
   path( "",CartView.as_view(),name= "cart"),
   path("items/",CartItemView.as_view(),name = "cart-items"),
   path("items/<int:pk>/",CartItemView.as_view()),
]
