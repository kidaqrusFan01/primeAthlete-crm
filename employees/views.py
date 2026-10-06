from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import role_required

from .forms import EmployeeForm
from .models import Employee


@login_required
@role_required("CEO", "ADMIN")
def employee_list(request):
    employees = Employee.objects.select_related("user").all()

    search = request.GET.get("search", "").strip()
    department = request.GET.get("department", "").strip()
    status = request.GET.get("status", "").strip()

    if search:
        employees = employees.filter(
            Q(employee_id__icontains=search)
            | Q(user__first_name__icontains=search)
            | Q(user__last_name__icontains=search)
            | Q(user__email__icontains=search)
            | Q(position__icontains=search)
        )

    if department:
        employees = employees.filter(
            department=department
        )

    if status:
        employees = employees.filter(
            employment_status=status
        )

    context = {
        "employees": employees,
        "search": search,
        "department": department,
        "status": status,
        "department_choices": Employee.DEPARTMENT_CHOICES,
        "status_choices": Employee.EMPLOYMENT_STATUS_CHOICES,
    }

    return render(
        request,
        "employees/employee_list.html",
        context,
    )


@login_required
@role_required("CEO", "ADMIN")
def employee_create(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)

        if form.is_valid():
            employee = form.save()

            messages.success(
                request,
                f"{employee.user.get_full_name()} was added successfully.",
            )

            return redirect(
                "employees:detail",
                employee_id=employee.id,
            )
    else:
        form = EmployeeForm()

    return render(
        request,
        "employees/employee_form.html",
        {
            "form": form,
            "page_title": "Add Employee",
            "submit_text": "Add Employee",
        },
    )


@login_required
@role_required("CEO", "ADMIN")
def employee_detail(request, employee_id):
    employee = get_object_or_404(
        Employee.objects.select_related("user"),
        id=employee_id,
    )

    return render(
        request,
        "employees/employee_detail.html",
        {
            "employee": employee,
        },
    )


@login_required
@role_required("CEO", "ADMIN")
def employee_edit(request, employee_id):
    employee = get_object_or_404(
        Employee.objects.select_related("user"),
        id=employee_id,
    )

    if request.method == "POST":
        form = EmployeeForm(
            request.POST,
            instance=employee,
        )

        if form.is_valid():
            employee = form.save()

            messages.success(
                request,
                f"{employee.user.get_full_name()} was updated successfully.",
            )

            return redirect(
                "employees:detail",
                employee_id=employee.id,
            )
    else:
        form = EmployeeForm(
            instance=employee,
        )

    return render(
        request,
        "employees/employee_form.html",
        {
            "form": form,
            "page_title": "Edit Employee",
            "submit_text": "Save Changes",
        },
    )


@login_required
@role_required("CEO", "ADMIN")
def employee_deactivate(request, employee_id):
    employee = get_object_or_404(
        Employee.objects.select_related("user"),
        id=employee_id,
    )

    if request.method == "POST":
        employee.employment_status = "INACTIVE"
        employee.save()

        employee.user.is_active_employee = False
        employee.user.save()

        messages.success(
            request,
            f"{employee.user.get_full_name()} has been deactivated.",
        )

        return redirect("employees:list")

    return render(
        request,
        "employees/employee_confirm_deactivate.html",
        {
            "employee": employee,
        },
    )