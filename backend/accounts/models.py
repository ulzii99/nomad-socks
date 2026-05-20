from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    preferred_language = models.CharField(
        max_length=2,
        choices=[("mn", "Mongolian"), ("en", "English")],
        default="mn",
    )

    def __str__(self):
        return self.email or self.username
