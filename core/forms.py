from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile

MAJOR_CHOICES = [
    ("", "Select a major (optional)"),
    ("BIT - IRM", "BIT - IRM (Information Resource Management)"),
    ("BIT - NET", "BIT - NET (Network Technology)"),
    ("BIT - IMD", "BIT - IMD (Interactive Multimedia & Design)"),
    ("CS", "Computer Science"),
    ("BUSI", "Business"),
    ("ENG", "Engineering"),
    ("OTHER", "Other"),
]

MINOR_CHOICES = [
    ("", "Select a minor (optional)"),
    ("Business Entrepreneurship", "Business Entrepreneurship"),
    ("Data Science", "Data Science"),
    ("Statistics", "Statistics"),
    ("Math", "Mathematics"),
    ("OTHER", "Other"),
]


class CustomUserCreationForm(UserCreationForm):
    carleton_email = forms.EmailField(
        required=True,
        label="Carleton Email",
        widget=forms.EmailInput(attrs={"placeholder": "name@cmail.carleton.ca"}),
    )

    student_number = forms.CharField(
        required=True,
        label="Student Number",
        widget=forms.TextInput(attrs={"placeholder": "101313237"}),
    )

    major = forms.ChoiceField(
        required=False,
        choices=MAJOR_CHOICES,
        widget=forms.Select(),
    )

    minor = forms.ChoiceField(
        required=False,
        choices=MINOR_CHOICES,
        widget=forms.Select(),
    )

    class Meta:
        model = User
        fields = ("username", "carleton_email", "student_number", "major", "minor", "password1", "password2")

    def clean_carleton_email(self):
        email = (self.cleaned_data.get("carleton_email") or "").strip().lower()
        if not (email.endswith("@cmail.carleton.ca") or email.endswith("@carleton.ca")):
            raise forms.ValidationError("Email must end in @cmail.carleton.ca or @carleton.ca.")
        return email

    def clean_student_number(self):
        sn = (self.cleaned_data.get("student_number") or "").strip()
        if not sn.isdigit():
            raise forms.ValidationError("Student number must be digits only.")
        return sn

    def save(self, commit=True):
        user = super().save(commit=commit)

        # Create / update profile with the extra fields
        Profile.objects.update_or_create(
            user=user,
            defaults={
                "carleton_email": self.cleaned_data["carleton_email"],
                "student_number": self.cleaned_data["student_number"],
                "major": self.cleaned_data.get("major", ""),
                "minor": self.cleaned_data.get("minor", ""),
            },
        )
        return user