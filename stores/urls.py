from django.urls import path

from . import views

app_name = "stores"
urlpatterns = [
    path("", views.store_view, name="store"),
    path("search/", views.search_view, name="search"),
    path("<slug:category_slug>/", views.store_view, name="products_by_category"),
    path(
        "<slug:category_slug>/<slug:product_slug>/",
        views.product_detail_view,
        name="product_detail",
    ),
]
