from django import forms
from django.contrib.auth import get_user_model
from django.db import transaction

from .models import Employee


User = get_user_model()


class EmployeeForm(forms.ModelForm):

    # ==========================
    # ACCOUNT INFORMATION
    # ==========================

    username = forms.CharField(
        max_length=150,
        required=False,
        help_text="Leave blank to generate a username automatically.",
    )

    first_name = forms.CharField(
        max_length=150,
        required=True,
    )

    last_name = forms.CharField(
        max_length=150,
        required=True,
    )

    email = forms.EmailField(
        required=True,
    )

    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
    )

    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Create login password"
            }
        ),
        help_text="Required when creating a new employee.",
    )

    password_confirmation = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm login password"
            }
        ),
    )

    # ==========================
    # EMPLOYEE INFORMATION
    # ==========================

    class Meta:
        model = Employee

        fields = [
            "employee_id",
            "department",
            "position",
            "phone",
            "date_of_birth",
            "date_joined",
            "employment_status",
            "salary",
            "address",
            "emergency_contact_name",
            "emergency_contact_phone",
            "notes",
        ]

        widgets = {
            "date_of_birth": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "date_joined": forms.DateInput(
                attrs={
                    "type": "date"
                }
            ),

            "salary": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "min": "0",
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "rows": 3
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "rows": 3
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Editing an existing employee
        if self.instance and self.instance.pk:

            user = self.instance.user

            self.fields["username"].initial = user.username
            self.fields["first_name"].initial = user.first_name
            self.fields["last_name"].initial = user.last_name
            self.fields["email"].initial = user.email
            self.fields["role"].initial = user.role

            # Username cannot be changed during editing.
            self.fields["username"].disabled = True

            # Password is not required when editing.
            self.fields["password"].help_text = (
                "Leave blank to keep the current password."
            )

    def clean_employee_id(self):
        employee_id = self.cleaned_data["employee_id"].strip()

        queryset = Employee.objects.filter(
            employee_id=employee_id
        )

        if self.instance and self.instance.pk:
            queryset = queryset.exclude(
                pk=self.instance.pk
            )

        if queryset.exists():
            raise forms.ValidationError(
                "This employee ID already exists."
            )

        return employee_id

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        queryset = User.objects.filter(
            email=email
        )

        if self.instance and self.instance.pk:
            queryset = queryset.exclude(
                pk=self.instance.user.pk
            )

        if queryset.exists():
            raise forms.ValidationError(
                "A user with this email already exists."
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get(
            "password_confirmation"
        )

        # New employee
        if not self.instance.pk:

            if not password:
                self.add_error(
                    "password",
                    "A password is required for a new employee.",
                )

            if password and len(password) < 8:
                self.add_error(
                    "password",
                    "Password must be at least 8 characters.",
                )

            if password != password_confirmation:
                self.add_error(
                    "password_confirmation",
                    "Passwords do not match.",
                )

        # Existing employee
        else:

            if password or password_confirmation:

                if not password:
                    self.add_error(
                        "password",
                        "Enter a password.",
                    )

                if len(password) < 8:
                    self.add_error(
                        "password",
                        "Password must be at least 8 characters.",
                    )

                if password != password_confirmation:
                    self.add_error(
                        "password_confirmation",
                        "Passwords do not match.",
                    )

        return cleaned_data

    @transaction.atomic
    def save(self, commit=True):

        employee = super().save(commit=False)

        username = self.cleaned_data.get("username")
        first_name = self.cleaned_data["first_name"]
        last_name = self.cleaned_data["last_name"]
        email = self.cleaned_data["email"]
        role = self.cleaned_data["role"]
        password = self.cleaned_data.get("password")

        # ==========================
        # CREATE NEW EMPLOYEE
        # ==========================

        if not employee.pk:

            if not username:

                username = (
                    self.cleaned_data["employee_id"]
                    .lower()
                    .replace(" ", "")
                )

            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
            )

            user.role = role

            user.department = self.cleaned_data[
                "department"
            ]

            user.phone = self.cleaned_data[
                "phone"
            ]

            user.date_joined_company = self.cleaned_data[
                "date_joined"
            ]

            user.is_active_employee = (
                self.cleaned_data[
                    "employment_status"
                ] == "ACTIVE"
            )

            user.set_password(password)

            user.save()

            employee.user = user

        # ==========================
        # EDIT EXISTING EMPLOYEE
        # ==========================

        else:

            user = employee.user

            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.role = role

            user.department = self.cleaned_data[
                "department"
            ]

            user.phone = self.cleaned_data[
                "phone"
            ]

            user.date_joined_company = self.cleaned_data[
                "date_joined"
            ]

            user.is_active_employee = (
                self.cleaned_data[
                    "employment_status"
                ] == "ACTIVE"
            )

            if password:
                user.set_password(password)

            user.save()

        if commit:
            employee.save()

        return employee