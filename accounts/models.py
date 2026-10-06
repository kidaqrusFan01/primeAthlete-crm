from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ("CEO", "CEO"),
        ("IT", "IT Staff"),
        ("COACH", "Fitness Coach"),
        ("ATHLETE", "Weightlifter"),
        ("ADMIN", "Administrative Staff"),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="ADMIN",
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    department = models.CharField(
        max_length=100,
        blank=True,
    )

    date_joined_company = models.DateField(
        null=True,
        blank=True,
    )

    is_active_employee = models.BooleanField(
        default=True,
    )

    def __str__(self):
        return f"{self.get_full_name()} ({self.username})"