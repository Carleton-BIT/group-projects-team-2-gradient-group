from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("profile/", views.profile, name="profile"),
    path("listings/", views.browse_listings, name="browse_listings"),
    path("listings/create/", views.create_listing, name="create_listing"),
    path("my-listings/", views.my_listings, name="my_listings"),
    path("my-listings/<int:listing_id>/edit/", views.edit_listing, name="edit_listing"),
    path("my-listings/<int:listing_id>/delete/", views.delete_listing, name="delete_listing"),
]