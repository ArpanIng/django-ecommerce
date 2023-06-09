from django.contrib import admin

from .models import Category, Product, Variation, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "price", "stock", "is_available", "category"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ["product", "variation_category", "variation_value", "is_active"]
    list_editable = ("is_active",)
    list_filter = ("variation_category", "variation_value", "is_active")


admin.site.register(Review)
