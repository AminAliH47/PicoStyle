from django.db import models


class BrandsManager(models.Manager):
    def get_active_brands(self):
        return self.filter(active=True)
