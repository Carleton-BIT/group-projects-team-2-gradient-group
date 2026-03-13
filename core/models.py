from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    carleton_email = models.EmailField(unique=True)
    student_number = models.CharField(max_length=32, unique=True)

    major = models.CharField(max_length=100, blank=True, default="")
    minor = models.CharField(max_length=100, blank=True, default="")

    def __str__(self):
        return self.user.username


class Listing(models.Model):
    CATEGORY_CHOICES = [
        ("Textbooks", "Textbooks"),
        ("Electronics", "Electronics"),
        ("Dorm Essentials", "Dorm Essentials"),
        ("Services", "Services"),
        ("Other", "Other"),
    ]

    CONDITION_CHOICES = [
        ("New", "New"),
        ("Like New", "Like New"),
        ("Good", "Good"),
        ("Fair", "Fair"),
        ("Used", "Used"),
    ]

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")

    title = models.CharField(max_length=150)
    description = models.TextField()

    price = models.DecimalField(max_digits=8, decimal_places=2)

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES)

    location = models.CharField(max_length=100, blank=True, default="Carleton University")

    image = models.ImageField(upload_to="listing_images/", blank=True, null=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title