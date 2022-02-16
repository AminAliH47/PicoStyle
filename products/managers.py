from django.db import models
from django.db.models import Q

"""
Models manager are in this file
"""


class ProductManager(models.Manager):

    # Get published products
    def get_published_product(self):
        return self.filter(status="published")

    # Get published related products
    def get_related_products(self, product):
        return self.filter(status="published", category=product.category.last()).distinct().exclude(id=product.id)

    def get_list(self):
        return self.defer("description").filter(status="published")

    # Count published product
    def product_count(self):
        products = self.filter(status="published").count()
        count = 0
        if products["count"] is not None:
            count = int(products["count"])
        return count

    # Method for search products by title and tag title
    def search_product(self, query):
        return self.get_published_product().filter(
            Q(title__icontains=query) |
            Q(model__icontains=query) |
            Q(tag__title__icontains=query) |
            Q(code2__icontains=query)
        )


class ProductsCategoryManager(models.Manager):
    # get active product category
    def get_active_category(self):
        return self.filter(active=True)

    # Count active product category
    def category_count(self):
        categories = self.filter(active=True).count()
        count = 0
        if categories["count"] is not None:
            count = int(categories["count"])
        return count
