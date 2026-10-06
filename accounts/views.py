from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard:home")

    if request.method == "POST":

        form = AuthenticationForm(
            request,
            data=request.POST,
        )

        if form.is_valid():

            user = form.get_user()

            if not user.is_active_employee:
                messages.error(
                    request,
                    "Your employee account is inactive. "
                    "Please contact Prime Athletes administration.",
                )

                return render(
                    request,
                    "accounts/login.html",
                    {
                        "form": form,
                    },
                )

            login(request, user)

            return redirect("dashboard:home")

    else:

        form = AuthenticationForm()

    return render(
        request,
        "accounts/login.html",
        {
            "form": form,
        },
    )


@login_required
def logout_view(request):

    logout(request)

    return redirect("accounts:login")