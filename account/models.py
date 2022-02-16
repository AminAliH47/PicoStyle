from django.db import models
from django.contrib.auth.models import (AbstractUser)
from django.urls import reverse_lazy
from account import managers
from config.validators import phone_regex, validate_file_size
from ckeditor_uploader.fields import RichTextUploadingField
from translated_fields import TranslatedField
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """ User and Seller Model """
    # Fields
    # author fields
    is_author = models.BooleanField(
        default=False,
        verbose_name="Is author",
    )
    # Seller fields
    is_seller = models.BooleanField(
        default=False,
        verbose_name="Is Supplier",
    )
    is_brand = models.BooleanField(
        default=False,
        verbose_name="Is brand",
    )
    is_entrepreneur = models.BooleanField(
        default=False,
        verbose_name="Is Entrepreneur",
    )
    about_manager = TranslatedField(
        RichTextUploadingField(
            max_length=200,
            null=True,
            blank=True,
            help_text=_("Max length 200 character"),
        )
    )
    manager_photo = models.ImageField(
        null=True,
        blank=True,
        validators=[validate_file_size],
    )
    company_name = models.CharField(
        max_length=25,
        blank=True,
        help_text=_("Max length 25 character"),
    )
    co_address = models.TextField(
        max_length=100,
        blank=True,
        help_text=_("Max length 100 character"),
    )
    co_country_registered = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text=_("Max length 20 character"),
    )
    co_website_address = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        help_text=_("Max length 40 character"),
    )
    co_email = models.EmailField(
        null=True,
        blank=True,
    )
    telephone_number = models.CharField(
        max_length=11,
        null=True,
        blank=True,
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=13,
        blank=True,
    )
    products_type = models.ManyToManyField(
        to="products.ProductsCategory",
        related_name="user_product_type",
        blank=True,
        limit_choices_to={'active': True},
    )
    brand_name = models.CharField(
        max_length=50,
        blank=True,
        help_text=_("Max length 50 character"),
    )
    about_brand = TranslatedField(
        RichTextUploadingField(
            blank=True,
        )
    )
    brand_logo = models.ImageField(
        upload_to='user/brand-logo',
        blank=True,
        validators=[validate_file_size],
    )
    branch_address = models.TextField(
        max_length=100,
        blank=True,
        help_text=_("Max length 100 character"),
    )
    branch_image = models.ImageField(
        upload_to='user/branch-image',
        blank=True,
        validators=[validate_file_size],
    )

    # Manager
    objects = managers.CustomUserManager()

    # Methods
    def __str__(self):
        if self.brand_name:
            return self.brand_name
        else:
            return self.username

    def get_entrepreneur_url(self):
        return reverse_lazy('entrepreneur:detail', kwargs={'pk': self.pk, 'entrepreneur_name': self.get_full_name()})

    def get_brand_url(self):
        return reverse_lazy('brands:detail', kwargs={'pk': self.pk, 'brand_name': self.brand_name})
