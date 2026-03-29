from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Product, Profile, SavedProduct

from .forms import CustomUserCreationForm, MAJOR_CHOICES, MINOR_CHOICES, ProductCreateForm, UserUpdateForm, ProfileUpdateForm


@login_required
def profile(request):
    return render(request, "core/profile.html")

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={
            "carleton_email": request.user.email or "",
            "student_number": None,
            "major": "",
            "minor": "",
        }
    )

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect("profile")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    return render(request, "core/edit_profile.html", {
        "user_form": user_form,
        "profile_form": profile_form,
    })

@login_required
def my_listings(request):
    products = Product.objects.filter(seller=request.user).order_by("-created_at")
    return render(request, "core/my_listings.html", {"products": products})


def index(request):
    # Start with all products
    products = Product.objects.all()
    
    # Capture the search query and filter from the URL (e.g., ?q=textbook&category=books)
    search_query = request.GET.get('q', '')
    category_filter = request.GET.get('category', '')

    # Apply Text Search (looks in title OR description)
    if search_query:
        products = products.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )

    # Apply Category Filter
    if category_filter:
        products = products.filter(category=category_filter)

    # Pass the products and current search terms back to the template
    context = {
        'products': products,
        'search_query': search_query,
        'category_filter': category_filter,
    }
    return render(request, "core/index.html", context)

def all_listings(request):
    products = Product.objects.filter(is_available=True)

    search_query = request.GET.get('q', '')
    category_filter = request.GET.get('category', '')

    if search_query:
        products = products.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )

    if category_filter:
        products = products.filter(category=category_filter)

    context = {
        'products': products,
        'search_query': search_query,
        'category_filter': category_filter,
    }
    return render(request, "core/all_listings.html", context)


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

