from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def home(request):
    return render(request, "core/home.html")

def index(request):
    return render(request, "core/index.html")

@login_required
def user_profile(request):
    user = request.user
    return render(request, 'core/profile.html', {'user': user})