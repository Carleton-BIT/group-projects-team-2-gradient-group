from django.contrib.auth import login
from django.shortcuts import render, redirect

from .forms import CustomUserCreationForm


def index(request):
    # Your homepage template
    return render(request, "core/index.html")


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
    else:
        form = CustomUserCreationForm()

    print("SIGNUP FORM FIELDS:", list(form.fields.keys()))  # <-- ADD THIS

    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("index")

    return render(request, "registration/signup.html", {"form": form})