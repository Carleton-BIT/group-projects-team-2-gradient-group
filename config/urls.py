from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core.forms import EmailPrefixAuthenticationForm

urlpatterns = [
    path("admin/", admin.site.urls),

    # core handles "/" and "/signup/"
    path("", include("core.urls")),

    # custom login form with username placeholder
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(authentication_form=EmailPrefixAuthenticationForm),
        name="login",
    ),

    # built-in auth urls: /accounts/login, /accounts/logout, etc.
    path("accounts/", include("django.contrib.auth.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)