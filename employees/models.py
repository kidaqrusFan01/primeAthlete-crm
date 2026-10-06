from django.conf import settings
from django.db import models


class Employee(models.Model):
    DEPARTMENT_CHOICES = [
        ("MANAGEMENT", "Management"),
        ("IT", "IT"),
        ("FITNESS", "Fitness"),
        ("ATHLETICS", "Athletics"),
        ("ADMIN", "Administration"),
    ]

    EMPLOYMENT_STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive"),
        ("ON_LEAVE", "On Leave"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="employee_profile",
    )

    employee_id = models.CharField(
        max_length=20,
        unique=True,
    )

    department = models.CharField(
        max_length=20,
        choices=DEPARTMENT_CHOICES,
    )

    position = models.CharField(
        max_length=100,
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    date_joined = models.DateField()

    employment_status = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_STATUS_CHOICES,
        default="ACTIVE",
    )

    salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    address = models.TextField(
        blank=True,
    )

    emergency_contact_name = models.CharField(
        max_length=100,
        blank=True,
    )

    emergency_contact_phone = models.CharField(
        max_length=20,
        blank=True,
    )

    notes = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"{self.employee_id} - {self.user.get_full_name()}"