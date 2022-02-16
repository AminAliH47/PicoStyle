from django import forms
from translated_fields import language_code_formfield_callback

from pages import models


class PagesForm(forms.ModelForm):
    formfield_callback = language_code_formfield_callback

    class Meta:
        model = models.Pages
        fields = "__all__"
