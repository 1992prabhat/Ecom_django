from django.contrib import admin

# Register your models here.
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
		search_fields = ('name', 'description')
		list_display = ('name', 'price', 'stock', 'active', 'created_at', 'updated_at')

