from django.contrib import admin

from .models import Product, Favorite, CartItem, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'category', 'price', 'created_at')
    
    list_filter = ('category', 'created_at')
    list_editable = ('price', 'category') 
    search_fields = ('name',)

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'added_at')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'total_price')