from django.contrib.auth.models import UserManager
from django.db import models


class CustomUserManager(UserManager):
    # Get active sellers from users
    def get_sellers(self):
        return self.filter(is_seller=True, is_active=True)

    # Get active brands from users
    def get_brands(self):
        return self.filter(is_seller=True, is_active=True, is_brand=True)

    # Get active entrepreneurs from users
    def get_entrepreneurs(self):
        return self.filter(is_seller=True, is_active=True, is_entrepreneur=True)

    # get count of active seller users
    def seller_count(self):
        reviews = self.filter(is_seller=True, is_active=True).aggregate(count=models.Count('id'))
        count = 0
        if reviews["count"] is not None:
            count = int(reviews["count"])
        return count
