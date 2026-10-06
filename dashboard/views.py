from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from employees.models import Employee


@login_required
def dashboard(request):
    total_employees = Employee.objects.count()
    active_employees = Employee.objects.filter(
        employment_status="ACTIVE"
    ).count()

    context = {
        "total_employees": total_employees,
        "active_employees": active_employees,
    }

    return render(request, "dashboard/dashboard.html", context)