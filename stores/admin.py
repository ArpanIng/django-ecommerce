from django.contrib import admin

from .models import Product, Review


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "price", "stock", "is_available", "category"]
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Review)
