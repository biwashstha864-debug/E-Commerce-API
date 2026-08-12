from django.contrib import admin
from .models import Product,Category

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "description",
        "price",
        "category",
        "created_at",
        "updated_at", 
    ]
    search_fields = [
        "name",
        "description",
    ]
    
    list_filter = [
        "category",
    ]
    
@admin.register(Category)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]
    
    search_fields = [
        "name",
    ]