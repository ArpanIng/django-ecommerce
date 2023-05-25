from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from .views import home

urlpatterns = [
    path("", home, name="homepage"),
    path("admin/", admin.site.urls),
    path("cart/", include("carts.urls")),
    path("store/", include("stores.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
