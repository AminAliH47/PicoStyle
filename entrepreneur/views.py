from django.shortcuts import get_object_or_404
from django.views import generic
from account.models import User


# view for show of Entrepreneurs
class EntrepreneursList(generic.ListView):
    """
    List of Entrepreneurs
    """
    template_name = 'entrepreneur/pages/list.html'
    paginate_by = 12
    context_object_name = "entrepreneurs"
    queryset = User.objects.get_entrepreneurs()


class EntrepreneursDetail(generic.DetailView):
    """
    Detail of entrepreneurs
    """
    context_object_name = "entrepreneur"
    template_name = 'entrepreneur/pages/detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.kwargs['pk'])
