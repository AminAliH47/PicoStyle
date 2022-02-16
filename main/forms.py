from django import forms
from django.utils.translation import gettext_lazy as _
from translated_fields import language_code_formfield_callback
from main import models
from main.models import Retailers

TYPE = (
    ('MS.', 'MS.'),
    ('MrS.', 'MrS.'),
    ('Mr.', 'Mr.'),
)
YESNO = (
    ("Yes", "Yes"),
    ("No", "No"),
)
INFO = {
    "first_name": forms.TextInput(
        attrs={"placeholder": _("First name")}
    ),
    "last_name": forms.TextInput(
        attrs={"placeholder": _("Last name")}
    ),
    "address": forms.Textarea(
        attrs={"placeholder": _("Address")}
    ),
    "city": forms.TextInput(
        attrs={"placeholder": _("City")}
    ),
    "country": forms.TextInput(
        attrs={"placeholder": _("Country")}
    ),
    "email": forms.EmailInput(
        attrs={"placeholder": _("Email")}
    ),
    "phone": forms.TextInput(
        attrs={"placeholder": _("Phone number")}
    ),
    "zip_code": forms.TextInput(
        attrs={"placeholder": _("Zip code")}
    ),
}

OWNER = (
    ("Owner", "Owner"),
    ("Tenant", "Tenant"),
)


class RetailerForm(forms.ModelForm):
    """
    Become retailer form
    """

    # Custom Fields
    gender = forms.ChoiceField(
        choices=TYPE,
        widget=forms.RadioSelect(
            attrs={"class": "choice"},
        ),
    )
    experience = forms.ChoiceField(
        choices=YESNO,
        widget=forms.RadioSelect(
            attrs={"class": "choice"},
        ),
    )

    how_long = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": _("For how long?")},
        ),
    )
    manage_people = forms.IntegerField(
        widget=forms.NumberInput(),
    )
    professional_experience = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": _("Most recent professional experience")},
        ),
    )
    luxury_experience = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": _("Experience in luxury goods")},
        ),
    )
    open_store = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": _("Which town/city would you like to open a store")},
        ),
    )
    # -------------------
    have_store = forms.ChoiceField(
        choices=YESNO,
        widget=forms.RadioSelect(
            attrs={"class": "choice"},
        ),
    )
    center_town = forms.ChoiceField(
        choices=YESNO,
        widget=forms.RadioSelect(
            attrs={"class": "choice"},
        ),
    )
    owner = forms.ChoiceField(
        choices=OWNER,
        widget=forms.RadioSelect(
            attrs={"class": "choice"},
        ),
    )
    previous_member = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": _("Have previously a member of a franchise or a network?")},
        ),
    )
    wish = forms.CharField(
        widget=forms.Textarea(
            attrs={"placeholder": _("Wishing to join our network")},
        ),
    )
    equality = forms.CharField(
        widget=forms.Textarea(
            attrs={"placeholder": _("What equity do you have available for this project?")},
        ),
    )

    def clean_experience(self):
        experience = self.cleaned_data.get('experience')
        if experience == "Yes":
            self.fields['how_long'].required = True
            self.fields['manage_people'].required = True
            self.fields['professional_experience'].required = True
            self.fields['luxury_experience'].required = True
            self.fields['open_store'].required = True
            self.fields['have_store'].required = True
            self.fields['center_town'].required = True
        else:
            self.fields['how_long'].required = False
            self.fields['manage_people'].required = False
            self.fields['professional_experience'].required = False
            self.fields['luxury_experience'].required = False
            self.fields['open_store'].required = False
            self.fields['have_store'].required = False
            self.fields['center_town'].required = False
        return experience

    def clean_have_store(self):
        have_store = self.cleaned_data.get('have_store')
        if have_store == "Yes":
            self.fields['center_town'].required = True
            self.fields['owner'].required = True
            self.fields['previous_member'].required = True
            self.fields['wish'].required = True
            self.fields['equality'].required = True
        else:
            self.fields['center_town'].required = False
            self.fields['owner'].required = False
            self.fields['previous_member'].required = False
            self.fields['wish'].required = False
            self.fields['equality'].required = False
        return have_store

    class Meta:
        model = Retailers
        fields = ("gender", "first_name",
                  "last_name", "email",
                  "phone", "address",
                  "zip_code", "country",
                  "city", "experience",
                  "have_store", "center_town"
                  )
        widgets = INFO


class MainSliderForm(forms.ModelForm):
    formfield_callback = language_code_formfield_callback

    class Meta:
        model = models.MainSlider
        fields = "__all__"


class BrandsSliderForm(forms.ModelForm):
    formfield_callback = language_code_formfield_callback

    class Meta:
        model = models.BrandsSlider
        fields = "__all__"


class MainCategoriesForm(forms.ModelForm):
    formfield_callback = language_code_formfield_callback

    class Meta:
        model = models.MainCategories
        fields = "__all__"


class SocialMediaForm(forms.ModelForm):
    formfield_callback = language_code_formfield_callback

    class Meta:
        model = models.SocialMedia
        fields = "__all__"


class SpecialProjectsForm(forms.ModelForm):
    formfield_callback = language_code_formfield_callback

    class Meta:
        model = models.SpecialProjects
        fields = "__all__"


class WorkWithUsForm(forms.ModelForm):
    formfield_callback = language_code_formfield_callback

    class Meta:
        model = models.WorkWithUs
        fields = "__all__"


class StoreAgentForm(forms.ModelForm):
    formfield_callback = language_code_formfield_callback

    class Meta:
        model = models.StoreAgent
        fields = "__all__"


class SizeGuideForm(forms.ModelForm):
    formfield_callback = language_code_formfield_callback

    class Meta:
        model = models.SizeGuide
        fields = "__all__"
