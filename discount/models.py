from django.db import models
from django.utils.translation import gettext_lazy as _
from account.models import User


class Discounts(models.Model):
    """
    Model for Product price discount
    """
    STATUS = (
        ('accepted', 'accepted'),
        ('pending', 'pending'),
        ('rejected', 'rejected'),
    )

    # Fields
    wholesale_value = models.PositiveSmallIntegerField(
        default=0,
        help_text='%',
    )
    retail_value = models.PositiveSmallIntegerField(
        default=0,
        help_text='%',
    )
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='discounts',
    )
    all_products = models.BooleanField(
        default=False,
        verbose_name=_("Discount on all the products?")
    )
    category = models.ForeignKey(
        to="products.ProductsCategory",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS,
        default='pending',
    )

    # Metadata
    class Meta:
        verbose_name_plural = "01. Discounts"
        verbose_name = "discounts"
        ordering = ("-created_at",)

    # Methods
    def __str__(self):
        return f"{self.wholesale_value} - {self.retail_value}"


class ShowDiscount(models.Model):
    """
    Model for show/hide product discount
    """

    # Fields
    show_discount = models.BooleanField(
        default=True,
    )
    category = models.ForeignKey(
        to="products.ProductsCategory",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    brand = models.ForeignKey(
        to="account.User",
        on_delete=models.CASCADE,
        limit_choices_to={'is_seller': True},
        null=True,
        blank=True,
    )

    # Metadata
    class Meta:
        verbose_name = "status"
        verbose_name_plural = "02. Discount show/hide status"

    # Methods
    def __str__(self):
        return "Status"
