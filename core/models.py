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