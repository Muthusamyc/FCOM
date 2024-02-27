from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import redirect

from commons.roles import CUSTOMER, DESIGNER, PARTNER


def authenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)

        else:
            return HttpResponse('you are not autherized')
    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            role = request.user.role
            if (role in allowed_roles) or (request.user.is_superuser):
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("you are not allowed to view this page")
        return wrapper_func
    return decorator


def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        role = request.user.role
        if request.user.is_superuser or role == DESIGNER or role == PARTNER:
            return view_func(request, *args, **kwargs)
        # elif role == 4:
        #     return redirect('master/selected_users/partner/')
        # elif role == 3:
        #     return redirect('selected_users/designer/')
        # elif role <= 2:
        #     return redirect('selected_users/admin/')
        else:
            return HttpResponse("you are not allowed")
    return wrapper_function


def customer_only(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            logout(request=request)

        return func(request, *args, **kwargs)

    return wrapper
