from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile

MAJOR_CHOICES = [
    ("", "Select a major"),

    # Business & Economics
    ("Commerce", "Commerce (BCom)"),
    ("Economics", "Economics"),
    ("Business Law", "Business Law"),

    # Computer & Technology
    ("Computer Science", "Computer Science"),
    ("Information Technology - IRM", "Information Technology - Information Resource Management (IRM)"),
    ("Information Technology - NET", "Information Technology - Network Technology (NET)"),
    ("Information Technology - IMD", "Information Technology - Interactive Multimedia & Design (IMD)"),
    ("Data Science", "Data Science"),
    ("Software Engineering", "Software Engineering"),

    # Engineering
    ("Aerospace Engineering", "Aerospace Engineering"),
    ("Biomedical Engineering", "Biomedical Engineering"),
    ("Civil Engineering", "Civil Engineering"),
    ("Electrical Engineering", "Electrical Engineering"),
    ("Mechanical Engineering", "Mechanical Engineering"),
    ("Sustainable & Renewable Energy Engineering", "Sustainable & Renewable Energy Engineering"),

    # Arts & Social Sciences
    ("Psychology", "Psychology"),
    ("Political Science", "Political Science"),
    ("Sociology", "Sociology"),
    ("Criminology", "Criminology"),
    ("Journalism", "Journalism"),
    ("Communication & Media Studies", "Communication & Media Studies"),
    ("Law", "Law"),
    ("Philosophy", "Philosophy"),
    ("History", "History"),
    ("English", "English"),
    ("Linguistics", "Linguistics"),

    # Science
    ("Biology", "Biology"),
    ("Chemistry", "Chemistry"),
    ("Physics", "Physics"),
    ("Neuroscience", "Neuroscience"),
    ("Environmental Science", "Environmental Science"),
    ("Health Sciences", "Health Sciences"),
    ("Mathematics", "Mathematics"),
    ("Statistics", "Statistics"),

    # Architecture & Design
    ("Architecture", "Architecture"),
    ("Industrial Design", "Industrial Design"),

    # Public Affairs
    ("International Business", "International Business"),
    ("International Relations", "International Relations"),
    ("Public Affairs & Policy Management", "Public Affairs & Policy Management"),
    ("Global & International Studies", "Global & International Studies"),

    # Education
    ("Bachelor of Education", "Bachelor of Education"),

    # Other
    ("Undeclared", "Undeclared"),
    ("Other", "Other"),
]

MINOR_CHOICES = [
    ("", "Select a minor"),

    # Business & Management
    ("Business", "Business"),
    ("Business Entrepreneurship", "Business Entrepreneurship"),
    ("Economics", "Economics"),
    ("Management", "Management"),

    # Technology & Data
    ("Computer Science", "Computer Science"),
    ("Data Science", "Data Science"),
    ("Mathematics", "Mathematics"),
    ("Statistics", "Statistics"),

    # Social Sciences
    ("Political Science", "Political Science"),
    ("Sociology", "Sociology"),
    ("Criminology", "Criminology"),
    ("Psychology", "Psychology"),
    ("Law", "Law"),
    ("Global & International Studies", "Global & International Studies"),

    # Arts & Humanities
    ("English", "English"),
    ("History", "History"),
    ("Philosophy", "Philosophy"),
    ("Linguistics", "Linguistics"),
    ("French", "French"),
    ("Indigenous Studies", "Indigenous Studies"),

    # Science
    ("Biology", "Biology"),
    ("Chemistry", "Chemistry"),
    ("Physics", "Physics"),
    ("Environmental Science", "Environmental Science"),
    ("Neuroscience", "Neuroscience"),

    # Design & Media
    ("Communication & Media Studies", "Communication & Media Studies"),
    ("Journalism", "Journalism"),
    ("Film Studies", "Film Studies"),

    # Public Affairs
    ("Public Policy & Administration", "Public Policy & Administration"),
    ("International Relations", "International Relations"),

    # Other
    ("Other", "Other"),
]


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        label="First Name",
        widget=forms.TextInput(attrs={"placeholder": "Your First Name"}),
    )

    last_name = forms.CharField(
        required=True,
        label="Last Name",
        widget=forms.TextInput(attrs={"placeholder": "Your Last Name"}),
    )

    carleton_email = forms.EmailField(
        required=True,
        label="Carleton Email",
        widget=forms.EmailInput(attrs={"placeholder": "name@cmail.carleton.ca"}),
    )

    student_number = forms.CharField(
        required=True,
        label="Student Number",
        widget=forms.TextInput(attrs={"placeholder": "123456789"}),
    )

    # ✅ searchable inputs (datalist)
    major = forms.CharField(
        required=True,
        label="Major",
        widget=forms.TextInput(attrs={
            "placeholder": "Start typing your major…",
            "list": "major-list",
            "autocomplete": "off",
        }),
    )

    minor = forms.CharField(
        required=True,
        label="Minor",
        widget=forms.TextInput(attrs={
            "placeholder": "Start typing your minor…",
            "list": "minor-list",
            "autocomplete": "off",
        }),
    )

    class Meta:
        model = User
        fields = (
            "username",
            "carleton_email",
            "student_number",
            "major",
            "minor",
            "password1",
            "password2",
        )

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

    # ✅ optional: enforce that typed major/minor must be from your lists
    def clean_major(self):
        val = (self.cleaned_data.get("major") or "").strip()
        if not val:
            return ""
        allowed = {label for value, label in MAJOR_CHOICES if value}
        if val not in allowed:
            raise forms.ValidationError("Please choose a major from the suggestions.")
        return val

    def clean_minor(self):
        val = (self.cleaned_data.get("minor") or "").strip()
        if not val:
            return ""
        allowed = {label for value, label in MINOR_CHOICES if value}
        if val not in allowed:
            raise forms.ValidationError("Please choose a minor from the suggestions.")
        return val

    def save(self, commit=True):
        user = super().save(commit=False)

        # Capitalize names properly
        user.first_name = (self.cleaned_data.get("first_name") or "").strip().title()
        user.last_name = (self.cleaned_data.get("last_name") or "").strip().title()

        # Optional but recommended: force usernames lowercase
        user.username = (self.cleaned_data.get("username") or "").strip().lower()

        if commit:
            user.save()

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