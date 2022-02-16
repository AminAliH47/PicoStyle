from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.translation import get_language
from config.validators import validate_file_size
from products import managers
from django.urls import reverse_lazy
from django.utils.text import slugify
from translated_fields import TranslatedField


# Create models here
class ProductsType(models.Model):
    """ Product type for users """

    # Fields
    title = models.CharField(
        max_length=20,
        help_text=_("Max length 20 character"),
    )
    active = models.BooleanField(
        default=True,
    )

    # Metadata
    class Meta:
        verbose_name_plural = "03. Products Type"
        verbose_name = "type"

    # Methods
    def __str__(self):
        return self.title


class ProductsCategory(models.Model):
    """
    Product categories model
    """

    # Fields
    parent = models.ForeignKey(
        'self',
        related_name="children",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    title = TranslatedField(
        models.CharField(
            max_length=20,
            help_text=_("Max length 20 character"),
        )
    )
    slug = models.SlugField(
        unique=False,
        verbose_name="Slug (URL)",
    )
    image = models.ImageField(
        upload_to="products/category",
        null=True,
        blank=True,
        help_text="(1600 * 250)px",
        validators=[validate_file_size],
    )
    icon = models.ImageField(
        null=True,
        blank=True,
    )
    active = models.BooleanField(
        default=True,
    )

    # Manager
    objects = managers.ProductsCategoryManager()

    # Metadata
    class Meta:
        verbose_name_plural = "02. Products Category"
        verbose_name = "category"
        ordering = ('parent__id',)
        unique_together = ('slug', 'parent')

    # Methods
    def __str__(self):
        return f"{self.parent} - {self.title}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, *kwargs)

    def get_absolute_url(self):
        if self.parent is not None:
            return f"/{get_language()}/products/{'/'.join([c.slug for c in self.all_parent][::-1])}"
        else:
            return reverse_lazy('products:p_category', kwargs={'item': self.slug})

    @property
    def all_parent(self):
        categories = []
        current_category = self
        while current_category is not None:
            categories.append(current_category)
            current_category = current_category.parent
        return categories


class ProductsTag(models.Model):
    """
    Products Tag model
    """

    # Fields
    title = models.CharField(
        max_length=20,
        help_text=_("Max length 20 character"),
    )

    # Metadata
    class Meta:
        verbose_name_plural = "04. Products Tag"
        verbose_name = "tag"

    # Methods
    def __str__(self):
        return self.title


class ProductMaterial(models.Model):
    """
    Products Material model
    """

    # Fields
    title = models.CharField(
        max_length=20,
        help_text=_("Max length 20 character"),
    )

    # Metadata
    class Meta:
        verbose_name_plural = "05. Products Material"
        verbose_name = "material"

    # Methods
    def __str__(self):
        return self.title


class ShoeSole(models.Model):
    """
    Shoe solo model
    """

    # Fields
    title = models.CharField(
        max_length=20,
        help_text=_("Max length 20 character"),
    )

    # Metadata
    class Meta:
        verbose_name_plural = "06. Shoe sole"
        verbose_name = "sole"

    # Methods
    def __str__(self):
        return self.title


class ProductSize(models.Model):
    """
    Dynamic size for products
    """

    # Fields
    title = models.CharField(
        max_length=5,
    )

    # Metadata
    class Meta:
        verbose_name = "size"
        verbose_name_plural = "08. Product size"

    # Methods
    def __str__(self):
        return self.title


class Products(models.Model):
    """
    Products model
    """
    STATUS = (
        ('published', 'published'),
        ('pending', 'pending'),
        ('rejected', 'rejected'),
    )
    CURRENCY = (
        ("us_dollar", "US Dollar"),
        ("ir_rials", "IR Rials"),
        ("ruble", "Ruble"),
        ("euro", "Euro"),
    )

    # Fields
    seller = models.ForeignKey(
        to="account.User",
        on_delete=models.CASCADE,
        related_name="s_products",
        limit_choices_to={'is_seller': True},
    )
    title = models.CharField(
        max_length=25,
        help_text=_("Max length 25 character"),
    )
    slug = models.SlugField(
        unique=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    description = models.TextField(
        max_length=250,
        null=True,
        blank=True,
        help_text=_("Max length 250 character"),
    )
    # Product Specifications
    type = models.CharField(
        max_length=20,
        null=True,
        help_text=_("Max length 20 character"),
    )
    code2 = models.CharField(
        max_length=7,
        unique=True,
        verbose_name="Product code",
    )
    model = models.CharField(
        max_length=10,
        verbose_name="Product model",
    )
    size = models.ManyToManyField(
        ProductSize,
        related_name='s_products',
        blank=True,
        verbose_name="Product Size",
    )
    size_info = models.TextField(
        verbose_name="Size more information",
        null=True,
        blank=True,
    )
    care_info = models.TextField(
        max_length=100,
        null=True,
        blank=True,
        help_text=_("Max length 100 character"),
    )
    care_and_fabric = models.TextField(
        max_length=100,
        null=True,
        blank=True,
        help_text=_("Max length 100 character"),
    )
    finer_detail = models.TextField(
        max_length=100,
        null=True,
        blank=True,
        help_text=_("Max length 100 character"),
    )
    # Shoe
    heel = models.PositiveSmallIntegerField(
        help_text="cm",
        null=True,
        blank=True,
    )
    sole = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    # ===========
    weight = models.IntegerField(
        verbose_name="Product weight",
        null=True,
        blank=True,
        help_text="gr",
    )
    material = models.ForeignKey(
        ProductMaterial,
        null=True,
        on_delete=models.SET_NULL,
        related_name="m_products",
    )
    dimensions = models.TextField(
        max_length=50,
        null=True,
        blank=True,
        help_text=_("Max length 50 character"),
        verbose_name=_("Dimensions"),
    )
    # Price
    exw_price = models.CharField(
        max_length=50,
    )
    wholesale_price = models.CharField(
        max_length=20,
    )
    retail_price_USD = models.CharField(
        max_length=20,
    )
    discount = models.PositiveSmallIntegerField(
        default=0,
    )
    wholesale_discount = models.PositiveSmallIntegerField(
        default=0,
    )
    retail_discount = models.PositiveSmallIntegerField(
        default=0,
    )
    show_discount = models.BooleanField(
        default=True,
    )
    currency = models.CharField(
        max_length=10,
        choices=CURRENCY,
    )
    show_retail_price = models.BooleanField(
        default=True,
    )
    show_wholesale_price = models.BooleanField(
        default=True,
    )
    # ===========
    image = models.ImageField(
        upload_to="product/",
        validators=[validate_file_size],
    )
    category = models.ManyToManyField(
        ProductsCategory,
        related_name="c_products",
    )
    tag = models.ManyToManyField(
        ProductsTag,
        blank=True,
        related_name="t_products",
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS,
        default='pending',
    )

    # Manager
    objects = managers.ProductManager()

    # Metadata
    class Meta:
        verbose_name = "product"
        verbose_name_plural = "01. Products"
        ordering = ("-created_at",)

    # Methods
    def __str__(self):
        return self.code2

    def save(self, *args, **kwargs):
        self.slug = slugify(self.code2)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy("products:detail", kwargs={"pk": self.pk})

    @property
    def all_categories(self):
        categories = []
        current_category = self.category.all()
        for x in current_category:
            while x is not None:
                categories.append(x)
                x = x.parent
        return categories

    def check_discount(self):
        if self.show_discount:
            if self.discount > 0:
                return self.discount
            else:
                return None
        else:
            return None


class ProductImages(models.Model):
    """
    Multiple image for product
    """

    # Fields
    product = models.ForeignKey(
        Products,
        on_delete=models.CASCADE,
        related_name="images",
    )
    image = models.ImageField(
        upload_to="products/images",
        validators=[validate_file_size],
    )


class ProductPercent(models.Model):
    """
    Dynamic percentage for product price
    """
    PRICE = (
        ("retailer", "retailer"),
        ("wholesale", "wholesale"),
    )

    # Fields
    value = models.PositiveSmallIntegerField(
        help_text="%",
    )
    slug = models.CharField(
        max_length=9,
        choices=PRICE,
        unique=True,
        help_text="Don't change this field",
    )

    # Metadata
    class Meta:
        verbose_name = "percent"
        verbose_name_plural = "07. Product price percent"

    # Methods
    def __str__(self):
        return str(self.value)


class ShowProducts(models.Model):
    """
    Show or hide product price model
    """

    # Fields
    show_retail_price = models.BooleanField(
        default=True,
    )
    show_wholesale_price = models.BooleanField(
        default=True,
    )
    category = models.ForeignKey(
        ProductsCategory,
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
        verbose_name_plural = "09. Products show/hide status"

    # Methods
    def __str__(self):
        return "Status"


class PriceIncrease(models.Model):
    """
    Model for request a product price increase
    """
    STATUS = (
        ('accepted', 'accepted'),
        ('pending', 'pending'),
        ('rejected', 'rejected'),
    )

    # Fields
    value = models.CharField(
        max_length=15,
        default=0,
    )
    seller = models.ForeignKey(
        to="account.User",
        on_delete=models.CASCADE,
        related_name='price_increase',
    )
    all_products = models.BooleanField(
        default=False,
        verbose_name=_("Increase on all the products?"),
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
        verbose_name_plural = "10. Price increase"
        verbose_name = "request"
        ordering = ("-created_at",)

    # Methods
    def __str__(self):
        return str(self.value)
