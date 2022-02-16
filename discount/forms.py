from django import forms
from discount.models import Discounts, ShowDiscount

FORM = {
    'category': forms.Select(attrs={'class': 'js-example-basic-single'}),
}


class DiscountsFormSuperuser(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(DiscountsFormSuperuser, self).__init__(*args, **kwargs)
        self.fields['category'].required = False

    class Meta:
        model = Discounts
        fields = ("wholesale_value", "retail_value", "all_products", "category", "seller", "status",)
        widgets = FORM


class DiscountsFormSeller(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(DiscountsFormSeller, self).__init__(*args, **kwargs)
        self.fields['category'].required = False

    class Meta:
        model = Discounts
        fields = ("wholesale_value", "retail_value",  "all_products", "category",)
        widgets = FORM


class ShowDiscountForm(forms.ModelForm):
    class Meta:
        SHOW_FORM = {
            'category': forms.Select(attrs={'class': 'js-example-basic-multiple'})
        }
        model = ShowDiscount
        widgets = SHOW_FORM
        fields = ('show_discount', 'category', 'brand',)
