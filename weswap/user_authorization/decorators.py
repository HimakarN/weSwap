from django.shortcuts import redirect
from functools import wraps


def otp_verified_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.session.get('otp_verified'):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('password_reset')  # Redirect to forgot password page
    return _wrapped_view