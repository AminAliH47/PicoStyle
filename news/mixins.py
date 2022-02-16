from django.http import Http404
from django.shortcuts import get_object_or_404
from news.models import News


class FieldsMixin:
    """mixin for show filed filter in superuser and author"""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            raise Http404
        elif request.user.is_superuser:
            from news.forms import NewsSuperuserForm  # Import locally
            self.form_class = NewsSuperuserForm
        elif request.user.is_author:
            from news.forms import NewsAuthorForm  # Import locally
            self.form_class = NewsAuthorForm
        else:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class FormValidMixin:
    """mixin for show form """

    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.save()
        else:
            self.obj = form.seve(commit=False)
            self.obj.author = self.request.user
            self.obj.status = 'pending'
        return super().form_valid(form)


class AuthorAccessMixin:
    """mixin for check AuthorAccess"""

    def dispatch(self, request, pk, *args, **kwargs):
        news = get_object_or_404(News, pk=pk)
        if news.author == request.user or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404


class SuperuserAccessMixin:
    """mixin for check is superuser for delete news"""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404
