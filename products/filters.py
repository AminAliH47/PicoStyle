import django_filters as filters
from django import forms
from django.db import OperationalError
from django.utils.translation import gettext_lazy as _
from account.models import User
from products.models import (
    Products,
    ProductMaterial,
    ProductsCategory,
)

try:
    brands = [(x.brand_name, x.brand_name) for x in User.objects.get_brands()]
except OperationalError:
    brands = []

try:
    sellers = User.objects.get_sellers()
except OperationalError:
    sellers = []


class ProductFilter(filters.FilterSet):
    material = filters.ModelChoiceFilter(
        queryset=ProductMaterial.objects.all(),
        widget=forms.RadioSelect(attrs={
            "onchange": "this.form.submit()",
        }),
    )
    category = filters.ModelChoiceFilter(
        queryset=ProductsCategory.objects.get_active_category(),
        widget=forms.RadioSelect(attrs={
            "onchange": "this.form.submit()",
        }),
    )
    seller = filters.ModelChoiceFilter(
        queryset=sellers,
        widget=forms.RadioSelect(attrs={
            "onchange": "this.form.submit()",
        }),
    )
    SORT = (
        ("low_to_high", 'Low to High'),
        ("high_to_low", 'High to Low'),
        ("newest", 'Newest'),
        ("popular", 'Popular'),
    )
    sort = filters.ChoiceFilter(choices=SORT, empty_label=None, method='sort_by_filter',
                                widget=forms.RadioSelect(attrs={
                                    "onchange": "this.form.submit()",
                                }), )

    @staticmethod
    def sort_by_filter(queryset, name, value):
        if value == "low_to_high":
            return queryset.order_by('retail_price_USD')
        elif value == "high_to_low":
            return queryset.order_by('-retail_price_USD')
        elif value == "newest":
            return queryset.order_by('-created_at')
        elif value == "popular":
            return queryset.order_by('?')

    brand = filters.ChoiceFilter(
        choices=brands,
        empty_label=None, method='brand_filter',
        widget=forms.RadioSelect(attrs={
            "onchange": "this.form.submit()",
            "size": 10
        }), )

    @staticmethod
    def brand_filter(queryset, name, value):
        return queryset.filter(seller__brand_name__icontains=value)

    class Meta:
        model = Products
        fields = ('material', "category", "brand", "sort",)


class ProductPanelFilter(filters.FilterSet):
    brand = filters.ChoiceFilter(
        choices=brands,
        empty_label=None, method='brand_filter',
        widget=forms.RadioSelect(attrs={
            "onchange": "this.form.submit()",
        }), )

    @staticmethod
    def brand_filter(queryset, name, value):
        return queryset.filter(seller__brand_name__icontains=value)

    category = filters.ModelChoiceFilter(
        queryset=ProductsCategory.objects.get_active_category(),
        method='category_filter',
        widget=forms.Select(attrs={
            "onchange": "this.form.submit()",
            "class": "js-example-basic-multiple",
        }),
    )

    @staticmethod
    def category_filter(queryset, name, value):
        return queryset.filter(category=value)

    STATUS = (
        ('published', 'published'),
        ('pending', 'pending'),
        ('rejected', 'rejected'),
    )
    status = filters.ChoiceFilter(choices=STATUS, empty_label=None,
                                  widget=forms.RadioSelect(attrs={
                                      "onchange": "this.form.submit()",
                                  }), )

    class Meta:
        model = Products
        fields = ("brand", "status", "category",)


class CategoryPanelFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains', widget=forms.TextInput(
        attrs={'placeholder': _('Title of category')}
    ))

    class Meta:
        model = ProductsCategory
        fields = ('title',)
