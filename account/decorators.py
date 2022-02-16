from django.shortcuts import redirect
from django.urls import reverse_lazy


def is_login():
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(reverse_lazy('main:index'))
            return view_func(request, *args, **kwargs)

        return wrap

    return decorator
