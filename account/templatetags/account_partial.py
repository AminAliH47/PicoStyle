from django import template
from messages.models import Messages

register = template.Library()


@register.simple_tag(takes_context=True)
def header(context, **kwargs):
    request = context['request']
    if not request.user.is_anonymous:
        h_message = Messages.objects.get_messages_header(seller=request.user)
    else:
        h_message = []

    def unread_messages_count():
        messages = Messages.objects.filter(is_read=False, seller=request.user).count()
        return messages

    data = {
        "h_messages": h_message,
        "unread_messages": unread_messages_count,
    }
    return data
