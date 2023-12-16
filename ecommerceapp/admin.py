from django.contrib import admin
from .models import Category,Products,Cart
# Register your models here.

class AdminCategory(admin.ModelAdmin):
    list_display = ['id','name', 'description', 'image']
    list_editable = ['description']
    list_per_page = 10

admin.site.register(Category, AdminCategory)

class AdminProducts(admin.ModelAdmin):
    list_display = ['id','name','category', 'price', 'stock', 'available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    list_per_page = 10

admin.site.register(Products, AdminProducts)

