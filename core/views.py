from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models import Q

from .models import Product
from .forms import CustomUserCreationForm, MAJOR_CHOICES, MINOR_CHOICES


@login_required
def profile(request):
    return render(request, "core/profile.html")


def index(request):
    return render(request, "core/index.html")


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

def all_listings(request):
    from decimal import Decimal, InvalidOperation

    products = Product.objects.filter(is_available=True)

    q = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    condition = request.GET.get("condition", "").strip()
    min_price = request.GET.get("min_price", "").strip()
    max_price = request.GET.get("max_price", "").strip()
    sort = request.GET.get("sort", "newest").strip()

    if q:
        products = products.filter(
            Q(title__icontains=q)
            | Q(description__icontains=q)
            | Q(course_code__icontains=q)
            | Q(author__icontains=q)
        )

    if category:
        products = products.filter(category=category)

    if condition:
        products = products.filter(condition=condition)

    if min_price:
        try:
            products = products.filter(price__gte=Decimal(min_price))
        except (InvalidOperation, ValueError):
            pass

    if max_price:
        try:
            products = products.filter(price__lte=Decimal(max_price))
        except (InvalidOperation, ValueError):
            pass

    if sort == "price_asc":
        products = products.order_by("price", "-created_at")
    elif sort == "price_desc":
        products = products.order_by("-price", "-created_at")
    else:
        products = products.order_by("-created_at")

    return render(request, "core/all_listings.html", {
        "products": products,
        "search_query": q,
        "category_filter": category,
        "condition_filter": condition,
        "min_price": min_price,
        "max_price": max_price,
        "sort": sort,
        "category_choices": Product.CATEGORY_CHOICES,
        "condition_choices": Product.CONDITION_CHOICES,
    })