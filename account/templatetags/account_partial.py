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

    def not_read_count():
        messages = Messages.objects.filter(is_read=False, seller=request.user).count()
        count = 0
        if messages["count"] is not None:
            count = int(messages["count"])
        return count

    data = {
        "h_messages": h_message,
        "not_read_messages": not_read_count,
    }
    return data
