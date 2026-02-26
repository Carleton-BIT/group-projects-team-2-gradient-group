from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # core handles "/" and "/signup/"
    path("", include("core.urls")),

    # built-in auth urls: /accounts/login, /accounts/logout, etc.
    path("accounts/", include("django.contrib.auth.urls")),
]