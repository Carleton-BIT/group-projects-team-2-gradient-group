from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("profile/", views.profile, name="profile"),
    path("products/create/", views.create_product_listing, name="create_product_listing"),
    path("product/<int:pk>/", views.product_detail, name="product_detail"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("my-listings/", views.my_listings, name="my_listings"),
]