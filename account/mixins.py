from django.http import Http404
from django.shortcuts import get_object_or_404

from account.models import User


class FieldsUserMixin:
    """mixin for show filed to superuser"""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            from account.forms import CreateUserForm  # Import locally
            self.form_class = CreateUserForm

        else:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class FieldsSellerMixin:
    """mixin for show filed to superuser"""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            raise Http404
        elif request.user.is_superuser:
            from account.forms import CreateSellerFormsSuperuser  # Import locally
            self.form_class = CreateSellerFormsSuperuser
        elif request.user.is_seller:
            from account.forms import UpdateSellerFormsSeller  # Import locally
            self.form_class = UpdateSellerFormsSeller
        else:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class UpdateFieldsSellerMixin:
    """mixin for show filed to superuser"""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            raise Http404
        elif request.user.is_superuser:
            from account.forms import UpdateSellerFormsSuperuser  # Import locally
            self.form_class = UpdateSellerFormsSuperuser
        elif request.user.is_seller:
            from account.forms import UpdateSellerFormsSeller  # Import locally
            self.form_class = UpdateSellerFormsSeller
        else:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class SellerFormValidMixin:
    """mixin for show form """

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.is_seller = True
        obj.is_author = True
        from django.contrib.auth.hashers import make_password  # Import locally
        obj.password = make_password(form.cleaned_data["password"])
        return super().form_valid(form)


class UpdateSellerFormValidMixin:
    """mixin for show form """

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.is_seller = True
        obj.is_author = True
        return super().form_valid(form)


class SellerAccountAccessMixin:
    """mixin for show form """

    def dispatch(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        if user == request.user or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404
