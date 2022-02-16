from django import forms
from translated_fields import language_code_formfield_callback

from products.models import (
    Products,
    ShowProducts,
    ProductsCategory,
    PriceIncrease,
)

CREATE_FORM = {
    'title': forms.TextInput(
        attrs={'placeholder': 'Title of product'},
    ),
    'description': forms.Textarea(),
    'tag': forms.SelectMultiple(
        attrs={'class': 'select2-class'},
    ),
    'size': forms.SelectMultiple(
        attrs={'class': 'select2-class'},
    ),
}


class ProductSuperuserForm(forms.ModelForm):
    """
    Product form fields for superusers
    """

    CURRENCY = (
        ("us_dollar", "US Dollar"),
        ("ir_rials", "IR Rials"),
        ("ruble", "Ruble"),
        ("euro", "Euro"),
    )
    currency = forms.ChoiceField(
        choices=CURRENCY,
        widget=forms.RadioSelect(),
    )
    discount = forms.IntegerField(
        max_value=100,
        widget=forms.NumberInput(
            attrs={'value': 0},
        ),
    )

    def __init__(self, *args, **kwargs):
        super(ProductSuperuserForm, self).__init__(*args, **kwargs)
        self.fields['type'].required = False
        self.fields['image'].required = True
        self.fields['description'].required = False
        self.fields['retail_price_USD'].required = False
        self.fields['wholesale_price'].required = False
        self.fields['wholesale_price'].disabled = True
        self.fields['retail_price_USD'].disabled = True

    def clean_category(self):
        category = self.cleaned_data.get('category')
        for x in category:
            if "Shoe" in str(x):
                self.fields['heel'].required = True
                self.fields['sole'].required = True
                self.fields['size'].required = True
        return category

    class Meta:
        model = Products
        widgets = CREATE_FORM
        fields = (
            "seller", "type",
            "description", "title",
            "weight", "model",
            "dimensions", "size",
            "size_info", "heel",
            "sole", "material",
            "exw_price", "wholesale_price",
            "retail_price_USD", "show_discount",
            "discount", "currency",
            "show_retail_price", "show_wholesale_price",
            "care_info", "care_and_fabric",
            "finer_detail", "image",
            "category", "tag",
            "status",
        )


class ProductSellerForm(forms.ModelForm):
    """
    Product form fields for seller users
    """

    CURRENCY = (
        ("us_dollar", "US Dollar"),
        ("ir_rials", "IR Rials"),
        ("ruble", "Ruble"),
        ("euro", "Euro"),
    )
    currency = forms.ChoiceField(
        choices=CURRENCY,
        widget=forms.RadioSelect(),
    )

    def __init__(self, *args, **kwargs):
        super(ProductSellerForm, self).__init__(*args, **kwargs)
        self.fields['type'].required = False
        self.fields['image'].required = True
        self.fields['description'].required = False
        self.fields['retail_price_USD'].required = False
        self.fields['wholesale_price'].required = False
        self.fields['wholesale_price'].disabled = True
        self.fields['retail_price_USD'].disabled = True

    def clean_category(self):
        category = self.cleaned_data.get('category')
        for x in category:
            if "Shoe" in str(x):
                self.fields['heel'].required = True
                self.fields['sole'].required = True
                self.fields['size'].required = True
        return category

    class Meta:
        model = Products
        widgets = CREATE_FORM
        fields = (
            "title", "description",
            "model", "type",
            "weight", "dimensions",
            "size", "size_info",
            "heel", "sole",
            "material", "exw_price",
            "wholesale_price", "retail_price_USD",
            "discount", "currency",
            "care_info", "care_and_fabric",
            "finer_detail", "image",
            "category", "tag",
        )


class ShowProductsForm(forms.ModelForm):
    class Meta:
        SHOW_FORM = {
            'category': forms.Select(
                attrs={'class': 'js-example-basic-multiple'},
            ),
        }
        model = ShowProducts
        widgets = SHOW_FORM
        fields = (
            'show_retail_price', 'show_wholesale_price',
            'category', 'brand',
        )


class ProductsCategoryForm(forms.ModelForm):
    formfield_callback = language_code_formfield_callback

    class Meta:
        model = ProductsCategory
        fields = (
            "parent", "title_en",
            "title_ru", "title_it",
            "image", "icon",
            "active",
        )


FORM = {
    'category': forms.Select(
        attrs={'class': 'js-example-basic-single'},
    ),
}


class IncreaseFormSuperuser(forms.ModelForm):
    """
    Product price increase form for superusers
    """

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(IncreaseFormSuperuser, self).__init__(*args, **kwargs)
        self.fields['category'].required = False

    class Meta:
        model = PriceIncrease
        fields = (
            "value", "all_products",
            "category", "seller",
            "status",
        )
        widgets = FORM


class IncreaseFormSeller(forms.ModelForm):
    """
    Product price increase form for seller users
    """

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(IncreaseFormSeller, self).__init__(*args, **kwargs)
        self.fields['category'].required = False

    class Meta:
        model = PriceIncrease
        fields = (
            "value", "all_products",
            "category",
        )
        widgets = FORM
