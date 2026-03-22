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
def create_product_listing(request):
    if request.method == "POST":
        form = ProductCreateForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect("index")
    else:
        form = ProductCreateForm()

    return render(request, "core/create_product_listing.html", {"form": form})


@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    is_saved = False
    if request.user.is_authenticated:
        is_saved = SavedProduct.objects.filter(
            user=request.user,
            product=product
        ).exists()

    return render(request, "core/product_detail.html", {
        "product": product,
        "is_saved": is_saved,
    })

def all_listings(request):
    products = Product.objects.filter(is_available=True).order_by("-created_at")

    search_query = request.GET.get("q", "")
    category_filter = request.GET.get("category", "")

    if search_query:
        products = products.filter(title__icontains=search_query)

    if category_filter:
        products = products.filter(category=category_filter)

    return render(request, "core/all_listings.html", {
        "products": products,
        "search_query": search_query,
        "category_filter": category_filter,
    })

@login_required
def my_listings(request):
    products = Product.objects.filter(seller=request.user).order_by("-created_at")
    return render(request, "core/my_listings.html", {"products": products})

@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if product.seller != request.user:
        return redirect("product_detail", pk=product.pk)

    if request.method == "POST":
        product.delete()
        return redirect("my_listings")

    return render(request, "core/delete_product.html", {"product": product})

@login_required
def saved_items(request):
    saved_products = SavedProduct.objects.filter(user=request.user).select_related("product")

    return render(request, "core/saved_items.html", {
        "saved_products": saved_products
    })

@login_required
def toggle_save_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    saved, created = SavedProduct.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        saved.delete()  # already saved → unsave

    return redirect(request.META.get("HTTP_REFERER", "index"))