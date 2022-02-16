from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from account.models import User


# Create your models here.
class MessagesManager(models.Manager):
    def get_messages_header(self, seller):  # get messages in account header
        return self.filter(seller=seller)[:3]


class Messages(models.Model):
    """ Model for messages """
    subject = models.CharField(
        max_length=25,
        help_text=_("Max length 25 character"),
    )
    message = RichTextUploadingField(
        max_length=250,
        help_text=_("Max length 250 character"),
    )
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name=_('Supplier or user'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    is_read = models.BooleanField(
        default=False,
    )

    objects = MessagesManager()

    class Meta:
        verbose_name_plural = "1. Messages"
        verbose_name = "message"
        ordering = ('-created_at',)

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse_lazy('account:mm_detail', kwargs={'pk': self.pk})
