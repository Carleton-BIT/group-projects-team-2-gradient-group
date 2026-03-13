from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CustomUserCreationForm, MAJOR_CHOICES, MINOR_CHOICES, ListingForm
from .models import Listing


@login_required
def profile(request):
    my_listing_count = Listing.objects.filter(seller=request.user, is_active=True).count()
    return render(request, "core/profile.html", {
        "my_listing_count": my_listing_count,
    })


def index(request):
    latest_listings = Listing.objects.filter(is_active=True)[:4]
    return render(request, "core/index.html", {
        "latest_listings": latest_listings,
    })


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = CustomUserCreationForm()

    majors = [label for value, label in MAJOR_CHOICES if value]
    minors = [label for value, label in MINOR_CHOICES if value]

    return render(request, "registration/signup.html", {
        "form": form,
        "majors": majors,
        "minors": minors,
    })


@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()
            return redirect("my_listings")
    else:
        form = ListingForm()

    return render(request, "core/create_listing.html", {
        "form": form
    })


def browse_listings(request):
    listings = Listing.objects.filter(is_active=True)
    return render(request, "core/browse_listings.html", {
        "listings": listings,
    })


@login_required
def my_listings(request):
    listings = Listing.objects.filter(seller=request.user).order_by("-created_at")
    return render(request, "core/my_listings.html", {
        "listings": listings,
    })


@login_required
def edit_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id, seller=request.user)

    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect("my_listings")
    else:
        form = ListingForm(instance=listing)

    return render(request, "core/edit_listing.html", {
        "form": form,
        "listing": listing,
    })


@login_required
def delete_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id, seller=request.user)

    if request.method == "POST":
        listing.delete()
        return redirect("my_listings")

    return render(request, "core/delete_listing.html", {
        "listing": listing,
    })