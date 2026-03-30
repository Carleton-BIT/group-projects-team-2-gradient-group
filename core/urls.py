from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listings/", views.all_listings, name="all_listings"),
    path("feedback/", views.feedback, name="feedback"),
    path("signup/", views.signup, name="signup"),
    path("profile/", views.profile, name="profile"),

    path("products/create/", views.create_product_listing, name="create_product_listing"),
    path("product/<int:pk>/", views.product_detail, name="product_detail"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("my-listings/", views.my_listings, name="my_listings"),
    path("products/<int:pk>/delete/", views.delete_product, name="delete_product"),
    path("saved-items/", views.saved_items, name="saved_items"),
    path("products/<int:pk>/save/", views.toggle_save_product, name="toggle_save_product"),

]