from django.http import HttpResponse


def staff_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("You are not allowed to view this page")

    return wrapper

def logged_in(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("You must be logged in")
    return wrapper
