from django.shortcuts import get_object_or_404
from django.views import generic
from account.models import User


# view for show of brands
class BrandsList(generic.ListView):
    """
    List of brands
    """
    template_name = 'brands/pages/list.html'
    paginate_by = 12
    context_object_name = "brands"
    queryset = User.objects.get_brands()


class BrandsDetail(generic.DetailView):
    """
    Detail brands
    """
    context_object_name = "brand"
    template_name = 'brands/pages/detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.kwargs['pk'])
