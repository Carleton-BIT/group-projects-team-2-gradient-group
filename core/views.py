from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import CustomUserCreationForm, MAJOR_CHOICES, MINOR_CHOICES, ProductCreateForm


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