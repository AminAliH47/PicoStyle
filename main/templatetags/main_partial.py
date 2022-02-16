from django import template
from main.models import (
    SubNavbar,
    MainNavbar,
    SocialMedia,
)
from products.models import ProductsCategory

register = template.Library()


@register.simple_tag(takes_context=True)
def header(context, **kwargs):
    data = {}
    h_categories = ProductsCategory.objects.filter(parent=None, active=True)

    data['main_navbar'] = MainNavbar.objects.all()
    data['sub_navbar'] = SubNavbar.objects.all()
    data['h_categories'] = h_categories
    return data


@register.simple_tag(takes_context=False)
def footer(**kwargs):
    data = {
        'social_medias': SocialMedia.objects.all(),
    }
    return data
