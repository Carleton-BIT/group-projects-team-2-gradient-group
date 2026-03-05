from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login

from core.forms import CustomUserCreationForm

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("index")  # or "login" if you don’t want auto-login
    template_name = "registration/signup.html"

    def form_valid(self, form):
        response = super().form_valid(form)

        # OPTIONAL: auto-login after signup
        login(self.request, self.object)

        return response