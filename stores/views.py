from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from carts.models import CartItem
from carts.views import _cart_id
from categories.models import Category

from .forms import ReviewModelForm
from .models import Product, Review


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

    context = {
        "product": product,
    }
    return render(request, "stores/product_detail.html", context)


def search_view(request):
    if "q" in request.GET:
        q = request.GET.get("q")
    else:
        q = ""

    products = Product.objects.filter(
        Q(name__icontains=q) | Q(description__icontains=q)
    )

    context = {
        "products": products,
        "products_count": products.count(),
        "queryset": q,
    }
    return render(request, "stores/store.html", context)


def submit_review_view(request, product_id):
    URL = request.META.get("HTTP_REFERER")  # stores previous URL

    # list of active reviews for a product
    # reviews = product.reviews.filter(status=True)
    if request.method == "POST":
        try:
            review = Review.objects.get(
                user__id=request.user.id,
                product__id=product_id,
            )
            form = ReviewModelForm(request.POST, instance=review)
            form.save()
            return redirect(URL)  # redirects to current page

        except Review.DoesNotExist:
            form = ReviewModelForm(request.POST)
            if form.is_valid():
                data = data
                review = form.cleaned_data["review"]
                rating = form.cleaned_data["rating"]
