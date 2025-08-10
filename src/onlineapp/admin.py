from django.contrib import admin
from .models import Category, Product, Order

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display =('product_name', 'description', 'price', 'image', 'category', 'created_at', 'updated_at',)
    search_fields = ('product_name', 'category__name')
    list_filter = ('category',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'customer_email', 'product', 'quantity', 'created_at', 'updated_at',)
    search_fields = ('customer_name', 'customer_email', 'product__product_name')
    list_filter = ('product',)