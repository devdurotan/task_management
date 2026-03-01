# accounts/models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .manager import UserManager

class Role(models.Model):
    ROLE_CHOICES = (
        ("1", "Admin"),
        ("2", "User"),
    )
    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)

    def __str__(self):
        return self.name

class UserMaster(AbstractBaseUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    role = models.ForeignKey(
        Role,
        on_delete=models.PROTECT,
        related_name="user_role",
        null=True,
        blank=True
    )


    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    def __str__(self):
        return self.email