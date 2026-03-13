from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),

    # core handles "/" and "/signup/"
    path("", include("core.urls")),

    # built-in auth urls: /accounts/login, /accounts/logout, etc.
    path("accounts/", include("django.contrib.auth.urls")),
]

# serve uploaded media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)