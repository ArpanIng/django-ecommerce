from django.shortcuts import render, get_object_or_404

from categories.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from .models import Product


def store_view(request, category_slug=None):
    # categories = None
    # products = None

    if category_slug:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        total_products_count = products.count()
    else:
        products = Product.objects.filter(is_available=True)
        total_products_count = products.count()

    context = {
        "products": products,
        "total_products_count": total_products_count,
    }
    return render(request, "stores/store.html", context)


def product_detail_view(request, category_slug, product_slug):
    product = get_object_or_404(
        Product,
        category__slug=category_slug,
        slug=product_slug,
    )
    # if a product is in a cart returns True else False
    try:
        in_cart = CartItem.objects.filter(
            cart__cart_id=_cart_id(request),
            product=product,
        ).exists()
    except:
        pass

    context = {
        "product": product,
        "in_cart": in_cart,
    }
    return render(request, "stores/product_detail.html", context)
