from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "email",
        "phone",
        "membership_status",
        "assigned_coach",
        "created_at",
    )

    list_filter = (
        "membership_status",
        "gender",
        "source",
    )

    search_fields = (
        "first_name",
        "last_name",
        "email",
        "phone",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "created_by",
    )