from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from translated_fields import TranslatedField


class Pages(models.Model):
    """
    Dynamic Pages model
    """

    # Fields
    title = TranslatedField(
        models.CharField(
            max_length=50,
            null=True,
            help_text=_("Max length 50 character"),
        )
    )
    slug = models.SlugField(
        unique=True,
    )
    content = TranslatedField(
        RichTextUploadingField(
            null=True,
        )
    )

    # Metadata
    class Meta:
        verbose_name = "page"
        verbose_name_plural = "1. Pages"

    # Methods
    def __str__(self):
        return self.title

    def i_update(self):
        return reverse_lazy("account:pp_update", kwargs={"pk": self.pk})

    def i_delete(self):
        return reverse_lazy("account:pp_delete", kwargs={"pk": self.pk})
