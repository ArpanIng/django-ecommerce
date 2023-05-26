from django.urls import path

from . import views

app_name = "carts"
urlpatterns = [
    path("", views.cart, name="cart"),
    path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("remove-cart/<int:product_id>/", views.remove_cart, name="remove_cart"),
    path(
        "remove-cart-item/<int:product_id>/",
        views.remove_cart_item,
        name="remove_cart_item",
    ),
]