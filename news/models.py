from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse_lazy
from news import managers
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class CategoryNews(models.Model):
    """
    News categories model
    """

    # Fields
    title = models.CharField(
        max_length=20,
        help_text=_("Max length 20 character"),
    )
    slug = models.SlugField(
        unique=True,
        verbose_name="slug (Link)",
    )
    image = models.ImageField(
        upload_to="news/category",
        null=True,
        blank=True,
    )
    icon = models.ImageField(
        null=True,
        blank=True,
    )
    active = models.BooleanField(
        default=True,
    )

    # Manager
    objects = managers.CategoryManager()

    # Metadata
    class Meta:
        verbose_name_plural = "02. News Category"
        verbose_name = "category"

    # Methods
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy('news:category', kwargs={'slug': self.slug})


class NewsTag(models.Model):
    """
    News Tag model
    """

    # Fields
    title = models.CharField(
        max_length=20,
        help_text=_("Max length 20 character"),
    )
    slug = models.CharField(
        max_length=120,
        unique=True,
    )

    # Metadata
    class Meta:
        verbose_name_plural = "03. News Tag"
        verbose_name = "tag"

    # Methods
    def __str__(self):
        return self.title


class News(models.Model):
    """
    News mode
    """
    STATUS = (
        ('published', 'published'),
        ('pending', 'pending'),
        ('rejected', 'rejected'),
    )

    # Fields
    title = models.CharField(
        max_length=30,
        help_text=_("Max length 30 character"),
    )
    slug = models.SlugField(
        unique=False,
    )
    image = models.ImageField(
        upload_to='news/',
    )
    body = RichTextUploadingField()
    category = models.ManyToManyField(
        CategoryNews,
        blank=True,
        related_name="news",
    )
    tag = models.ManyToManyField(
        NewsTag,
        blank=True,
        related_name="news_tag",
    )
    author = models.ForeignKey(
        to="account.User",
        on_delete=models.CASCADE,
        related_name="news_author",
        limit_choices_to={'is_author': True},
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS,
        default='pending',
    )

    # Manager
    objects = managers.NewsManager()

    # Metadata
    class Meta:
        verbose_name_plural = "01. News"
        verbose_name = "new"
        ordering = ("-created_at",)

    # Methods
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse_lazy("news:detail", kwargs={"pk": self.pk, "slug": self.slug})
