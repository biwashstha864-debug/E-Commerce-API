from django.contrib import admin
from cart.models import Cart, CartItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "updated_at",
        "created_at",
    ]
    search_fields = [
        "user"
    ]
    
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = [
        "cart",
        "product",
        "quantity",
    ]
    search_fields = [
        "cart",
        "product",
        "quantity",
    ]
