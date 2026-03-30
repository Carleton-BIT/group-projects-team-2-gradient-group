from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Profile, Product

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

    class Meta:
        model = User
        fields = (
            "carleton_email",
            "password1",
            "password2",
        )

    def clean_carleton_email(self):
        email = (self.cleaned_data.get("carleton_email") or "").strip().lower()

        if not (email.endswith("@cmail.carleton.ca") or email.endswith("@carleton.ca")):
            raise forms.ValidationError("Email must end in @cmail.carleton.ca or @carleton.ca.")

        if Profile.objects.filter(carleton_email__iexact=email).exists():
            raise forms.ValidationError("An account with this Carleton email already exists.")

        derived_username = email.split("@", 1)[0]

        if User.objects.filter(username__iexact=derived_username).exists():
            raise forms.ValidationError(
                "That email prefix is already being used as a username. "
                "Please use a different Carleton email."
            )

        return email

    def save(self, commit=True):
        user = super().save(commit=False)

        email = (self.cleaned_data.get("carleton_email") or "").strip().lower()
        derived_username = email.split("@", 1)[0]

        user.first_name = (self.cleaned_data.get("first_name") or "").strip().title()
        user.last_name = (self.cleaned_data.get("last_name") or "").strip().title()
        user.username = derived_username
        user.email = email

        if commit:
            user.save()
            Profile.objects.update_or_create(
                user=user,
                defaults={
                    "carleton_email": email,
                },
            )

        return user

class EmailPrefixAuthenticationForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields["username"].widget.attrs.update({
            "placeholder": "Username is everything before @ in your email",
            "autocomplete": "username",
        })

class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "title",
            "author",
            "course_code",
            "description",
            "price",
            "category",
            "condition",
            "image",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "title": forms.TextInput(attrs={"placeholder": "Book title"}),
            "author": forms.TextInput(attrs={"placeholder": "Author name"}),
            "course_code": forms.TextInput(attrs={"placeholder": "e.g. IRM3004"}),
            "price": forms.NumberInput(attrs={"step": "0.01", "min": "0"}),
            "category": forms.Select(),
        }

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price <= 0:
            raise forms.ValidationError("Price must be greater than 0.")
        return price

    def clean_course_code(self):
        return self.cleaned_data["course_code"].upper().strip()


# Profile editing
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]

class ProfileUpdateForm(forms.ModelForm):
    major = forms.ChoiceField(
        choices=MAJOR_CHOICES,
        required=False,
        label="Major",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    minor = forms.ChoiceField(
        choices=MINOR_CHOICES,
        required=False,
        label="Minor",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    class Meta:
        model = Profile
        fields = ["carleton_email", "student_number", "major", "minor"]
        widgets = {
            "carleton_email": forms.EmailInput(attrs={"placeholder": "name@cmail.carleton.ca"}),
            "student_number": forms.TextInput(attrs={"placeholder": "123456789"}),
        }

    def clean_carleton_email(self):
        email = (self.cleaned_data.get("carleton_email") or "").strip().lower()

        if not (email.endswith("@cmail.carleton.ca") or email.endswith("@carleton.ca")):
            raise forms.ValidationError("Email must end in @cmail.carleton.ca or @carleton.ca.")

        qs = Profile.objects.filter(carleton_email__iexact=email).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("An account with this Carleton email already exists.")

        return email

    def clean_student_number(self):
        sn = (self.cleaned_data.get("student_number") or "").strip()

        if not sn:
            return None

        if not sn.isdigit():
            raise forms.ValidationError("Student number must be digits only.")

        qs = Profile.objects.filter(student_number=sn).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("This student number is already in use.")

        return sn