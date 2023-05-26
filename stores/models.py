from django.db import models
from django.urls import reverse

from categories.models import Category


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to="photos/products")
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):  # "<slug:category_slug>/<slug:product_slug>/"
        return reverse("stores:product_detail", args=[self.category.slug, self.slug])

    def __str__(self) -> str:
        return self.name
