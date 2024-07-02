from django.contrib.auth.models import AbstractUser
from django.db import models
import secrets
from external.enum.custom_enum import UserType


class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=10, choices=UserType.choices(), default=UserType.CUSTOMER)
    authentication_token = models.CharField(max_length=16, blank=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.authentication_token:
            self.authentication_token = secrets.token_hex(8)
        super().save(*args, **kwargs)
