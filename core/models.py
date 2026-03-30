from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    carleton_email = models.EmailField(unique=True)
    student_number = models.CharField(max_length=32, unique=True, blank=True, null=True)

    major = models.CharField(max_length=100, blank=True, default="")
    minor = models.CharField(max_length=100, blank=True, default="")

    def __str__(self):
        return self.user.username

class Product(models.Model):
    CONDITION_CHOICES = [
        ("new", "New"),
        ("like_new", "Like New"),
        ("good", "Good"),
        ("fair", "Fair"),
        ("poor", "Poor"),
    ]

    CATEGORY_CHOICES = [
        ("textbooks", "Textbooks"),
        ("electronics", "Electronics"),
        ("dorm_essentials", "Dorm Essentials"),
        ("services", "Services"),
    ]

    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="products"
    )
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200, blank=True)
    course_code = models.CharField(max_length=20, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    image = models.ImageField(upload_to="product_images/", blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.pk})

class SavedProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user} saved {self.product}"

class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username}"