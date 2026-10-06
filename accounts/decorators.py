from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def role_required(*allowed_roles):

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect("accounts:login")

            # Django superusers have full access.
            if request.user.is_superuser:
                return view_func(
                    request,
                    *args,
                    **kwargs,
                )

            if request.user.role not in allowed_roles:

                messages.error(
                    request,
                    "You do not have permission to access this section.",
                )

                return redirect("dashboard:home")

            return view_func(
                request,
                *args,
                **kwargs,
            )

        return wrapper

    return decorator