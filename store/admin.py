from django.contrib import admin
from .models import Category, Product, Order

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category')  # Removed 'name' and 'available'
    list_filter = ('category',)
    search_fields = ('title',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'status')
    list_filter = ('status',)

# Only register once
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
