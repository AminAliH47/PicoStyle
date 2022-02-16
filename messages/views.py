from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.http import require_POST
from account.models import User
from messages.models import Messages
from products.mixins import SuperuserAccessMixin


@require_POST
def create_message(request):
    """ Create message from ajax """
    if request.method == "POST" and request.is_ajax:
        value = {
            'subject': request.POST['subject'],
            'message': request.POST['message'],
            'id': request.POST['seller'],
        }
        Messages(subject=value['subject'], message=value['message'],
                 seller=User.objects.get(id=value['id'])).save()

        from django.http import HttpResponse
        return HttpResponse(value)


# view for create new news
class CreateMassages(SuperuserAccessMixin, generic.CreateView):
    """
    Create Massages in admin panel
    """
    model = Messages
    fields = ('subject', 'message', 'seller')
    template_name = 'account/items/pages/create-update.html'
    success_url = reverse_lazy("account:mm_list")


class UpdateMassages(SuperuserAccessMixin, generic.UpdateView):
    """
    Update Massages in admin panel
    """
    model = Messages
    fields = ('subject', 'message', 'seller')
    context_object_name = "massage"
    template_name = 'account/items/pages/create-update.html'

    def get_success_url(self):
        return self.request.GET['next']


class DeleteMassages(SuperuserAccessMixin, generic.DeleteView):
    """
    Delete Massages in admin panel
    """
    model = Messages
    context_object_name = "massage"
    template_name = 'account/items/pages/delete.html'

    def get_success_url(self):
        return self.request.GET['next']
