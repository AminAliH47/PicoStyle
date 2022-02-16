from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import gettext_lazy as _

CATEGORY = (
    ('Women', 'Women'),
    ('Men', 'Men'),
    ('Raw material', 'Raw material'),
    ('Life style', 'Life style'),
)


class Messages(models.Model):
    """
    Model for newsletter messages
    """

    # Fields
    subject = models.CharField(
        max_length=20,
        help_text=_("Max length 20 character"),
    )
    message = RichTextUploadingField()
    category = models.CharField(
        max_length=15,
        choices=CATEGORY,
    )

    # Metadata
    class Meta:
        verbose_name_plural = "1. Messages"
        verbose_name = "message"

    # Methods
    def __str__(self):
        return self.subject


class Subscribers(models.Model):
    """
    Model for newsletter subscribers
    """

    # Fields
    email = models.EmailField(
        unique=True,
    )
    full_name = models.CharField(
        max_length=30,
        help_text=_("Max length 30 character"),
    )
    category = models.CharField(
        max_length=15,
        choices=CATEGORY,
    )

    # Metadata
    class Meta:
        verbose_name_plural = "2. Subscribers"
        verbose_name = "subscriber"

    # Methods
    def __str__(self):
        return self.email
