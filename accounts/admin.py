from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "Prime Athletes Information",
            {
                "fields": (
                    "role",
                    "phone",
                    "department",
                    "date_joined_company",
                    "is_active_employee",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Prime Athletes Information",
            {
                "fields": (
                    "role",
                    "phone",
                    "department",
                    "date_joined_company",
                    "is_active_employee",
                )
            },
        ),
    )

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
        "department",
        "is_active_employee",
    )

    list_filter = (
        "role",
        "department",
        "is_active_employee",
    )

    search_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
    )