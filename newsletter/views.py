from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic
from newsletter import models
from newsletter.models import Subscribers
from config import settings
from products.mixins import SuperuserAccessMixin


def create_subscriber(request):
    """
    Create subscriber for newsletter
    """
    if request.method == "POST" and request.is_ajax:

        email = request.POST['email']
        full_name = request.POST['full_name']
        category = request.POST['category']

        if email and full_name and category:
            query = models.Subscribers.objects.filter(email=email)
            if query.exists():
                return HttpResponse(_("This email has already been subscribed in the newsletter"))
            else:
                models.Subscribers(email=email, full_name=full_name, category=category).save()
                return HttpResponse("created")
        else:
            return HttpResponse(_("Please fill the information"))
    return HttpResponse("ok")


class CreateMessage(SuperuserAccessMixin, generic.CreateView):
    """
    Create newsletter message
    """
    model = models.Messages
    fields = ('subject', 'message', 'category',)
    template_name = "account/items/pages/create-update.html"
    success_url = reverse_lazy("account:nw_list")

    def form_valid(self, form):
        subject = form.cleaned_data['subject']
        context = {
            'subject': form.cleaned_data['subject'],
            'message': form.cleaned_data['message'],
        }

        from django.template.loader import render_to_string  # Import locally
        html_message = render_to_string(template_name="newsletter/email/email_template.html", context=context)

        text_content = 'This is an important message.'

        # Send email as html template
        subscribers = Subscribers.objects.filter(category=form.cleaned_data['category'])

        from django.core.mail import EmailMultiAlternatives  # Import locally

        # if you want to send real email change "settings.DEFAULT_FROM_EMAIL" to "settings.EMAIL_HOST_USER"
        msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL,
                                     [sub.email for sub in subscribers])
        msg.attach_alternative(html_message, "text/html")
        msg.send()
        return super().form_valid(form)


class MessagesList(SuperuserAccessMixin, generic.ListView):
    """
    List messages of newsletter
    """
    model = models.Messages
    queryset = models.Messages.objects.all()
    paginate_by = 10
    context_object_name = "messages"
    template_name = "account/newsletter/pages/list.html"


class DeleteMessage(SuperuserAccessMixin, generic.DeleteView):
    """
    Delete newsletter message in admin panel
    """
    model = models.Messages
    context_object_name = "item"
    template_name = "account/items/pages/delete.html"
    success_url = reverse_lazy("account:nw_list")


class SubscribersList(SuperuserAccessMixin, generic.ListView):
    """
    List subscribers of newsletter in admin panel
    """
    model = models.Subscribers
    queryset = models.Subscribers.objects.all()
    paginate_by = 10
    context_object_name = "subscribers"
    template_name = "account/newsletter/subscribers/pages/list.html"


class DeleteSubscriber(SuperuserAccessMixin, generic.DeleteView):
    """
    Delete newsletter subscribers in admin panel
    """
    model = models.Subscribers
    context_object_name = "item"
    template_name = "account/items/pages/delete.html"
    success_url = reverse_lazy("account:nws_list")
