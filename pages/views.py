from django.urls import reverse_lazy
from django.views import generic
from pages import (
    models,
    forms,
)
from products.mixins import SuperuserAccessMixin


class PagesDetail(generic.DetailView):
    model = models.Pages
    context_object_name = 'page'
    template_name = 'pages/pages/pages.html'


class CreatePages(SuperuserAccessMixin, generic.CreateView):
    """
    Create pages in admin panel
    """
    model = models.Pages
    form_class = forms.PagesForm
    template_name = "account/items/pages/create-update.html"
    success_url = reverse_lazy('account:pp_list')


class UpdatePages(SuperuserAccessMixin, generic.UpdateView):
    """
    Update pages in admin panel
    """
    model = models.Pages
    form_class = forms.PagesForm
    template_name = "account/items/pages/create-update.html"
    context_object_name = "item"
    success_url = reverse_lazy('account:pp_list')


class DeletePages(SuperuserAccessMixin, generic.DeleteView):
    """
    Delete pages in admin panel
    """
    model = models.Pages
    template_name = "account/items/pages/delete.html"
    context_object_name = "item"
    success_url = reverse_lazy('account:pp_list')
