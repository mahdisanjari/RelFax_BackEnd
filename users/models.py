from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # remove username field
    username = None

    email = models.EmailField(unique=True)

    bio = models.TextField(blank=True, null=True)
    profile_status = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email