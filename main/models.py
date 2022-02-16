from ckeditor.fields import RichTextField
from django.db import models
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from config.validators import phone_regex
from translated_fields import TranslatedField

from main.managers import StoreAgentManager


class SiteSetting(models.Model):
    """
    Model for main site settings
    """

    # Fields
    site_title = models.CharField(
        max_length=100,
    )
    logo = models.ImageField(
        upload_to='main/logo',
        help_text='Logo color should be "Light"'
    )
    admin_logo = models.ImageField(
        upload_to='main/logo',
        help_text='Logo color should be "Dark"'
    )
    favicon = models.ImageField(
        upload_to='main/favicon',
        null=True,
        blank=True,
    )
    meta_description = models.TextField(
        max_length=160,
        help_text="Max length 160 character",
        null=True,
        blank=True,
    )

    # Metadata
    class Meta:
        verbose_name_plural = "01. Site setting"
        verbose_name = "setting"

    # Methods
    def __str__(self):
        return self.site_title


class MainSlider(models.Model):
    """
    Main Slideshow (first slideshow)
    """

    # Fields
    title = TranslatedField(
        models.CharField(
            max_length=15,
            blank=True,
            verbose_name=_("Title"),
        )
    )
    link = models.CharField(
        max_length=120,
    )
    description = TranslatedField(
        models.TextField(
            max_length=120,
            null=True,
            blank=True,
            verbose_name=_("Description"),
        )
    )
    button = TranslatedField(
        models.CharField(
            max_length=15,
            null=True,
            blank=True,
            verbose_name=_("Button"),
        )
    )
    button_link = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )
    cover = models.BooleanField(
        default=True,
        help_text=_("Have dark cover?"),
    )
    image = models.ImageField()

    # Metadata
    class Meta:
        verbose_name_plural = "02. Main slider"
        verbose_name = "slide"

    # Methods
    def __str__(self):
        return str(self.pk)

    def i_update(self):
        return reverse_lazy("account:m_ms_update", kwargs={"pk": self.pk})

    def i_delete(self):
        return reverse_lazy("account:m_ms_delete", kwargs={"pk": self.pk})


class BrandsSlider(models.Model):
    """
    Brands Slideshow
    """

    # Fields
    title = TranslatedField(
        models.CharField(
            max_length=15,
            blank=True,
            verbose_name=_("Title"),
        )
    )
    link = models.CharField(
        max_length=120
    )
    description = TranslatedField(
        models.TextField(
            max_length=100,
            null=True,
            blank=True,
            verbose_name=_("Description"),
        )
    )
    button = TranslatedField(
        models.CharField(
            max_length=15,
            null=True,
            blank=True,
            verbose_name=_("Button"),
        )
    )
    button_link = models.CharField(
        max_length=150,
        null=True,
        blank=True,
    )
    cover = models.BooleanField(
        default=True,
        help_text=_("Have dark cover?"),
    )
    image = models.ImageField()

    # Metadata
    class Meta:
        verbose_name_plural = "03. Brands slider"
        verbose_name = "slide"

    # Methods
    def __str__(self):
        return str(self.pk)

    def i_update(self):
        return reverse_lazy("account:m_bs_update", kwargs={"pk": self.pk})

    def i_delete(self):
        return reverse_lazy("account:m_bs_delete", kwargs={"pk": self.pk})


class MainNavbar(models.Model):
    """
    Model for main navbar (black navbar)
    """

    # Fields
    title = TranslatedField(
        models.CharField(
            max_length=50,
            null=True,
            verbose_name=_("Title"),
        )
    )
    slug = models.CharField(
        max_length=150,
    )

    # Metadata
    class Meta:
        verbose_name_plural = "04. Main navbar"
        verbose_name = "item"

    # Methods
    def __str__(self):
        return self.title


class SubNavbar(models.Model):
    """
    Model for sub navbar (white navbar)
    """

    # Fields
    title = TranslatedField(
        models.CharField(
            max_length=50,
            null=True,
            verbose_name=_("Title"),
        )
    )
    slug = models.CharField(
        max_length=150,
    )

    # Metadata
    class Meta:
        verbose_name_plural = "05. Sub navbar"
        verbose_name = "item"

    # Methods
    def __str__(self):
        return self.title


class SocialMedia(models.Model):
    """
    Model for website social media
    """
    ICON = (
        ("linkedin", "linkedin"),
        ("youtube", "youtube"),
        ("facebook", "facebook"),
        ("instagram", "instagram"),
        ("telegram", "telegram"),
    )

    # Fields
    title = TranslatedField(
        models.CharField(
            max_length=50,
            null=True,
        )
    )
    link = models.CharField(
        max_length=120,
    )
    icon_code = models.CharField(
        max_length=15,
        choices=ICON,
    )

    # Metadata
    class Meta:
        verbose_name_plural = "06. Social media"
        verbose_name = "social media"

    # Methods
    def __str__(self):
        return self.title

    def i_update(self):
        return reverse_lazy("account:m_sm_update", kwargs={"pk": self.pk})

    def i_delete(self):
        return reverse_lazy("account:m_sm_delete", kwargs={"pk": self.pk})


class MainCategories(models.Model):
    """
    Model for home page category section
    """

    # Fields
    title = TranslatedField(
        models.CharField(
            max_length=10,
            null=True,
            verbose_name=_("Title"),
            help_text=_("Max length 10 character"),
        )
    )
    image = models.ImageField(
        upload_to='main/categories',
    )
    link = models.CharField(
        max_length=30,
        help_text=_("Max length 30 character"),
    )

    # Metadata
    class Meta:
        verbose_name_plural = "07. Main categories"
        verbose_name = "category"

    # Methods
    def __str__(self):
        return self.title

    def i_update(self):
        return reverse_lazy("account:m_mc_update", kwargs={"pk": self.pk})

    def i_delete(self):
        return reverse_lazy("account:m_mc_delete", kwargs={"pk": self.pk})


class Retailers(models.Model):
    """
    Models for retailers (become retailers section)
    """
    TYPE = (
        ('MS.', 'MS.'),
        ('MrS.', 'MrS.'),
        ('Mr.', 'Mr.'),
    )
    YESNO = (
        ("Yes", "Yes"),
        ("No", "No"),
    )

    # Fields
    gender = models.CharField(
        max_length=4,
        choices=TYPE,
    )
    first_name = models.CharField(
        max_length=30,
        help_text=_("Max length 30 character"),
    )
    last_name = models.CharField(
        max_length=30,
        help_text=_("Max length 30 character"),
    )
    email = models.EmailField()
    phone = models.CharField(
        validators=[phone_regex],
        max_length=11,
    )
    address = models.TextField()
    zip_code = models.CharField(
        max_length=20,
        help_text=_("Max length 20 character"),
    )
    country = models.CharField(
        max_length=20,
        help_text=_("Max length 20 character"),
    )
    city = models.CharField(
        max_length=20,
        help_text=_("Max length 20 character"),
    )
    # Project section
    experience = models.CharField(
        max_length=4,
        choices=YESNO,
    )
    experience_info = models.JSONField()
    have_store = models.CharField(
        max_length=4,
        choices=YESNO,
        null=True,
    )
    center_town = models.CharField(
        max_length=4,
        choices=YESNO,
        null=True,
    )

    # Metadata
    class Meta:
        verbose_name_plural = "08. Retailers"
        verbose_name = "retailer"

    # Methods
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class StoreAgent(models.Model):
    """ Models for store and agent section """

    # Fields
    name = TranslatedField(
        models.CharField(
            max_length=25,
            null=True,
            verbose_name=_("Name"),
            help_text=_("Max length 25 character"),
        )
    )
    country = models.CharField(
        max_length=20,
        help_text=_("Max length 20 character"),
    )
    country_code = models.CharField(
        max_length=4,
    )
    description = TranslatedField(
        RichTextField(
            max_length=200,
            null=True,
            verbose_name=_("Description"),
            help_text=_("Max length 200 character"),
        )
    )
    image = models.ImageField(
        upload_to="main/store-and-agent",
    )
    active = models.BooleanField(
        default=True,
    )

    # Metadata
    class Meta:
        verbose_name_plural = "09. Store and agent"
        verbose_name = "store"

    # Manager
    objects = StoreAgentManager()

    # Methods
    def __str__(self):
        return self.name

    def i_update(self):
        return reverse_lazy("account:m_sa_update", kwargs={"pk": self.pk})

    def i_delete(self):
        return reverse_lazy("account:m_sa_delete", kwargs={"pk": self.pk})


class SpecialProjects(models.Model):
    """
    Model for special project items section
    """

    # Fields
    title = TranslatedField(
        models.CharField(
            max_length=15,
            help_text=_("Max length 15 character"),
        )
    )
    link = models.CharField(
        max_length=50,
        help_text=_("Max length 50 character"),
    )
    image = models.ImageField(
        upload_to="main/special-project",
    )

    # Metadata
    class Meta:
        verbose_name_plural = "10. Special projects"
        verbose_name = "item"

    # Methods
    def __str__(self):
        return self.title

    def i_update(self):
        return reverse_lazy("account:m_sp_update", kwargs={"pk": self.pk})

    def i_delete(self):
        return reverse_lazy("account:m_sp_delete", kwargs={"pk": self.pk})


class WorkWithUs(models.Model):
    """
    Model for work with us items section
    """

    # Fields
    title = TranslatedField(
        models.CharField(
            max_length=15,
            help_text=_("Max length 15 character"),
        )
    )
    link = models.CharField(
        max_length=50,
        help_text=_("Max length 50 character"),
    )
    image = models.ImageField(
        upload_to="main/work-with-us",
    )

    # Metadata
    class Meta:
        verbose_name_plural = "11. Work with us"
        verbose_name = "item"

    # Methods
    def __str__(self):
        return self.title

    def i_update(self):
        return reverse_lazy("account:m_wu_update", kwargs={"pk": self.pk})

    def i_delete(self):
        return reverse_lazy("account:m_wu_delete", kwargs={"pk": self.pk})


class SizeGuide(models.Model):
    """
    Size guide item model
    """

    # Fields
    title = TranslatedField(
        models.CharField(
            max_length=15,
            help_text=_("Max length 15 character"),
        )
    )
    link = models.CharField(
        max_length=50,
        help_text=_("Max length 50 character"),
    )
    image = models.ImageField(
        upload_to="main/size-guide",
    )

    # Metadata
    class Meta:
        verbose_name_plural = "12. Size guide"
        verbose_name = "item"

    # Methods
    def __str__(self):
        return self.title

    def i_update(self):
        return reverse_lazy("account:m_sg_update", kwargs={"pk": self.pk})

    def i_delete(self):
        return reverse_lazy("account:m_sg_delete", kwargs={"pk": self.pk})
