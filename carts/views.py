from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404

# Product model is imported from stores app in models.py
from stores.models import Product, Variation
from .models import Cart, CartItem


def _cart_id(request):
    """
    returns sessionid stored in cookies as cart_id if not create sessionid
    """
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_variation = []  # list of posted 'POST' variation
    if request.method == "POST":
        for item in request.POST:  # color and size variation
            key = item
            value = request.POST[key]
            try:
                variation = Variation.objects.get(
                    product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value,
                )
                product_variation.append(variation)
            except Variation.DoesNotExist:
                pass
    try:
        # get the cart using the cart_id present in the session
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
    if cart_item_exists:  # if a product is in cart item
        cart_item = CartItem.objects.filter(product=product, cart=cart)
        existing_variations_list = []
        cart_item_id = []
        for item in cart_item:
            existing_variation = item.variations.all()
            existing_variations_list.append(list(existing_variation))
            cart_item_id.append(item.id)

        if product_variation in existing_variations_list:
            # increase cart item quantity
            index = existing_variations_list.index(product_variation)
            item_id = cart_item_id[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()
        else:
            # create a new cart item
            item = CartItem.objects.create(product=product, cart=cart, quantity=1)
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)
            item.save()
    else:  # create new cart item
        cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
        cart_item.save()

    return redirect("carts:cart")


@login_required
def cart(request, total=0, total_quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            total_quantity += cart_item.quantity
        tax = (2 * total) / 100  # 2% tax on total amount
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        "total": total,
        "total_quantity": total_quantity,
        "cart_items": cart_items,
        "tax": tax,
        "grand_total": grand_total,
    }
    return render(request, "carts/cart.html", context)


def remove_cart(request, product_id, cart_item_id):
    """Decrease cart_item quantity"""
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(id=cart_item_id, product=product, cart=cart)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
    except:
        pass
    return redirect("carts:cart")


def remove_cart_item(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(id=cart_item_id, product=product, cart=cart)
    cart_item.delete()
    return redirect("carts:cart")


def checkout_view(request, total=0, total_quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            total_quantity += cart_item.quantity
        tax = (2 * total) / 100  # 2% tax on total amount
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        "total": total,
        "total_quantity": total_quantity,
        "cart_items": cart_items,
        "tax": tax,
        "grand_total": grand_total,
    }
    return render(request, "carts/checkout.html", context)
