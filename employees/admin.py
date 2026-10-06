from django.contrib import admin
from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "employee_id",
        "get_full_name",
        "department",
        "position",
        "employment_status",
        "date_joined",
    )

    list_filter = (
        "department",
        "employment_status",
    )

    search_fields = (
        "employee_id",
        "user__first_name",
        "user__last_name",
        "user__email",
    )

    ordering = ("employee_id",)

    def get_full_name(self, obj):
        return obj.user.get_full_name()

    get_full_name.short_description = "Employee Name"