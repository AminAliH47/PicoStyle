from django.db import models


class NewsManager(models.Manager):
    def get_published_news(self):
        return self.filter(status='published')


class CategoryManager(models.Manager):
    def get_active_category(self):
        return self.filter(active=True)
