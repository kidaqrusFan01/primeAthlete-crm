from django.conf import settings
from django.db import models


class Client(models.Model):

    MEMBERSHIP_STATUS_CHOICES = [
        ("LEAD", "Lead"),
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive"),
        ("SUSPENDED", "Suspended"),
        ("EXPIRED", "Expired"),
    ]

    GENDER_CHOICES = [
        ("MALE", "Male"),
        ("FEMALE", "Female"),
    ]

    SOURCE_CHOICES = [
        ("WEBSITE", "Website"),
        ("SOCIAL_MEDIA", "Social Media"),
        ("REFERRAL", "Referral"),
        ("WALK_IN", "Walk-in"),
        ("EVENT", "Event"),
        ("OTHER", "Other"),
    ]

    # Basic information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    email = models.EmailField(
        unique=True,
        blank=True,
        null=True,
    )

    phone = models.CharField(max_length=30)

    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True,
    )

    date_of_birth = models.DateField(
        blank=True,
        null=True,
    )

    # Address
    address = models.TextField(
        blank=True,
    )

    city = models.CharField(
        max_length=100,
        blank=True,
    )

    country = models.CharField(
        max_length=100,
        default="Nigeria",
    )

    # CRM information
    membership_status = models.CharField(
        max_length=20,
        choices=MEMBERSHIP_STATUS_CHOICES,
        default="LEAD",
    )

    source = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        default="OTHER",
    )

    assigned_coach = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_clients",
        limit_choices_to={"role": "COACH"},
    )

    # Fitness/business information
    fitness_goal = models.TextField(
        blank=True,
    )

    membership_start_date = models.DateField(
        blank=True,
        null=True,
    )

    membership_end_date = models.DateField(
        blank=True,
        null=True,
    )

    # CRM notes
    notes = models.TextField(
        blank=True,
    )

    # Emergency contact
    emergency_contact_name = models.CharField(
        max_length=150,
        blank=True,
    )

    emergency_contact_phone = models.CharField(
        max_length=30,
        blank=True,
    )

    # System fields
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_clients",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"