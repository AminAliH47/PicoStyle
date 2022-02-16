from django import forms
from django.utils.translation import gettext_lazy as _
from account.models import User

CREATE_FORM = {
    'title': forms.TextInput(
        attrs={'placeholder': 'Title of Create User'}),
}


class LoginUserForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': _("Enter Email or Username")},
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': _("Enter Password")},
        ),
    )


# create seller
class CreateSellerFormsSuperuser(forms.ModelForm):
    """
    Create seller form for superuser users
    """

    def __init__(self, **kwargs):
        super(CreateSellerFormsSuperuser, self).__init__(**kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['password'].required = True
        self.fields['email'].required = True
        self.fields['phone_number'].required = True
        self.fields['company_name'].required = True
        self.fields['co_country_registered'].required = True
        self.fields['co_email'].required = True
        self.fields['brand_name'].required = True
        self.fields['brand_logo'].required = True
        self.fields['branch_address'].required = True

    class Meta:
        SELLER_FORM = {
            'is_seller': forms.HiddenInput(),
            'products_type': forms.SelectMultiple(
                attrs={'class': 'js-example-basic-multiple'},
            ),
            'phone_number': forms.TextInput(
                attrs={'placeholder': _('Country code')}
            )
        }
        model = User
        fields = ('username', 'password',
                  'first_name', 'last_name',
                  'email', 'phone_number',
                  'is_seller', 'company_name',
                  'co_address', 'co_country_registered',
                  'co_website_address', 'co_email',
                  'telephone_number', 'is_entrepreneur',
                  'about_manager_en', 'about_manager_ru',
                  'about_manager_it', 'manager_photo',
                  'products_type', 'brand_name',
                  'about_brand_en', 'about_brand_ru',
                  'about_brand_it', 'brand_logo',
                  'is_brand', 'branch_address',
                  'branch_image',
                  )
        widgets = SELLER_FORM


class UpdateSellerFormsSuperuser(forms.ModelForm):
    """
    Update seller form for superuser users
    """

    def __init__(self, **kwargs):
        super(UpdateSellerFormsSuperuser, self).__init__(**kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['phone_number'].required = True
        self.fields['company_name'].required = True
        self.fields['co_country_registered'].required = True
        self.fields['co_email'].required = True
        self.fields['brand_name'].required = True
        self.fields['brand_logo'].required = True
        self.fields['branch_address'].required = True

    class Meta:
        SELLER_FORM = {
            'is_seller': forms.HiddenInput(),
            'products_type': forms.SelectMultiple(
                attrs={'class': 'js-example-basic-multiple'},
            ),
            'phone_number': forms.TextInput(
                attrs={'placeholder': _('Country code')},
            ),
        }
        model = User
        fields = ('username', 'first_name',
                  'last_name', 'email',
                  'phone_number', 'is_seller',
                  'company_name', 'co_address',
                  'co_country_registered', 'co_website_address',
                  'co_email', 'telephone_number',
                  'is_entrepreneur', 'about_manager_en',
                  'about_manager_ru', 'about_manager_it',
                  'manager_photo', 'products_type',
                  'brand_name', 'about_brand_en',
                  'about_brand_ru', 'about_brand_it',
                  'brand_logo', 'is_brand',
                  'branch_address', 'branch_image',
                  )
        widgets = SELLER_FORM


class UpdateSellerFormsSeller(forms.ModelForm):
    """
    Update seller form for seller users
    """

    class Meta:
        SELLER_FORM = {
            'products_type': forms.SelectMultiple(
                attrs={'class': 'js-example-basic-multiple'},
            ),
            'phone_number': forms.TextInput(
                attrs={'placeholder': _('Country code')}
            )
        }
        model = User
        fields = ('products_type', 'about_brand_en',
                  'about_brand_ru', 'about_brand_it',
                  'telephone_number', 'co_website_address',
                  'manager_photo', 'about_manager_en',
                  'about_manager_ru', 'about_manager_it',
                  'branch_address', 'branch_image'
                  )
        widgets = SELLER_FORM


class PasswordForm(forms.Form):
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={"placeholder": _("Enter new password")},
        ),
    )
    re_password = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput(
            attrs={"placeholder": _("Enter new password again")},
        ),
    )
