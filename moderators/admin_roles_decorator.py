# admin_roles.py

from django.http import HttpResponseForbidden
from functools import wraps

# Custom decorator to check admin roles
def role_required(*allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and hasattr(request.user, 'admin'):
                admin = request.user.admin
                if admin.role in allowed_roles:
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponseForbidden("You do not have access to this page.")
            return HttpResponseForbidden("You need to be logged in.")
        return _wrapped_view
    return decorator
