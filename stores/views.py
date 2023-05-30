from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from categories.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from .models import Product


def store_view(request, category_slug=None):
    if category_slug:
        categories = get_object_or_404(Category, slug=category_slug)
        product_list = Product.objects.filter(
            category=categories,
            is_available=True,
        ).order_by("id")
        paginator = Paginator(product_list, per_page=6)
        page_number = request.GET.get("page")
        products = paginator.get_page(number=page_number)
        total_products_count = product_list.count()
    else:
        product_list = Product.objects.filter(is_available=True).order_by("id")
        paginator = Paginator(product_list, per_page=6)
        page_number = request.GET.get("page")
        products = paginator.get_page(
            number=page_number
        )  # when using get_page, EmptyPage and PageNotAnInteger are not required

        total_products_count = product_list.count()

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
