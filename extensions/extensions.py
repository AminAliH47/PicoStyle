import itertools
import json
import os
import re
from pathlib import Path
from random import randint

from django.contrib.humanize.templatetags.humanize import intcomma

BASE_DIR = Path(__file__).resolve().parent.parent

# JSON-based secrets module
with open(os.path.join(BASE_DIR, "secrets.json")) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
    """Get the secret variable or return explicit exception."""
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {0} environment variable".format(setting)
        from django.core.exceptions import ImproperlyConfigured
        raise ImproperlyConfigured(error_msg)


def category_status(c, status: bool, model):
    categories = c.children.all()
    for cat in categories:
        cat.active = status
        if cat.children.all():
            category_status(cat, status, model)
    model.objects.bulk_update(categories, fields=['active'])


def inactivate_status(c, model):
    categories = c.children.all()
    for cat in categories:
        cat.active = False
        if cat.children.all():
            inactivate_status(cat, model)
    model.objects.bulk_update(categories, fields=['active'])


def grouper(n, iterable):
    args = [iter(iterable)] * n
    return ([e for e in t if e is not None] for t in itertools.zip_longest(*args))


def separate(number):
    return re.sub(r"(\d+)(\d{3})", ",", str(number))


wp = 0


def cal_wholesale_price(product, w_discount, wholesale_percent):
    """ Calculate wholesale price for discount """
    wholesale_percent = wholesale_percent.value
    exw_price = int(product.exw_price.replace(",", ""))
    currency = product.currency
    discount = product.discount
    global wp
    if currency == "us_dollar":
        pass
    elif currency == "euro":
        exw_price = exw_price / 0.87
    elif currency == "ruble":
        exw_price = exw_price / 72.78
    elif currency == "ir_rials":
        exw_price = exw_price / 200000
    else:
        wp = 0

    wp = (exw_price * (1 - (discount / 100)) * (1 + (wholesale_percent / 100)))

    return intcomma(float(round((wp * (1 - (w_discount / 100))), 2)))


def cal_retail_price(retail_percent, r_discount):
    """ Calculate retail price for discount """
    retail_percent = retail_percent.value
    rp = (float(wp) * (1 + (retail_percent / 100)))

    return intcomma(float(round((rp * (1 - (r_discount / 100))), 2)))


def code_generator(obj, code):
    """ Generate product random code """
    if obj.objects.filter(code2=code).exists():
        code = f"{obj.seller.id}{[x.title for x in obj.all_categories][-1][0]}{obj.type[0]}{randint(1000, 9999)}"
        return code


def cal_wholesale_price2(product, value, wholesale_percent):
    """ Calculate wholesale price for price increase """
    wholesale_percent = wholesale_percent.value
    exw_price = value
    currency = product.currency
    discount = product.discount
    w_discount = product.wholesale_discount
    global wp
    if currency == "us_dollar":
        pass
    elif currency == "euro":
        exw_price = exw_price / 0.87
    elif currency == "ruble":
        exw_price = exw_price / 72.78
    elif currency == "ir_rials":
        exw_price = exw_price / 200000
    else:
        wp = 0

    wp = (exw_price * (1 - (discount / 100)) * (1 + (wholesale_percent / 100)))

    print(intcomma(float(round((wp * (1 - (w_discount / 100))), 2))))
    return intcomma(float(round((wp * (1 - (w_discount / 100))), 2)))


def cal_retail_price2(retail_percent, product):
    """ Calculate retail price for price increase """
    retail_percent = retail_percent.value
    rp = (float(wp) * (1 + (retail_percent / 100)))
    r_discount = product.retail_discount

    return intcomma(float(round((rp * (1 - (r_discount / 100))), 2)))
