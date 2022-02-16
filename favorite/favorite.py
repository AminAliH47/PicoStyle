from decimal import Decimal
from django.conf import settings
from products.models import Products


class Favorite(object):
    def __init__(self, request):
        """
        Initialize the favorite
        """
        self.session = request.session
        favorite = self.session.get(settings.FAVORITE_SESSION_ID)
        if not favorite:
            # Save empty favorite list in session
            favorite = self.session[settings.FAVORITE_SESSION_ID] = {}
        self.favorite = favorite

    def __iter__(self):
        """
        Iterate over the items in the favorite and get the products
        from the database.
        """
        product_ids = self.favorite.keys()
        # get the product objects and add them to the cart
        products = Products.objects.filter(id__in=product_ids)
        favorite = self.favorite.copy()
        for product in products:
            favorite[str(product.id)]['product'] = product

        for item in favorite.values():
            yield item

    def __len__(self):
        """
        Count all items in the favorite list.
        """
        return sum(item['quantity'] for item in self.favorite.values())

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the favorite or update list quantity.
        """
        product_id = str(product.id)
        if product_id not in self.favorite:
            self.favorite[product_id] = {"quantity": 0,
                                         "retail_price_USD": str(product.retail_price_USD)}
        if override_quantity:
            self.favorite[product_id]["quantity"] = quantity
        else:
            self.favorite[product_id]["quantity"] += quantity
        self.save()

    def remove(self, product):
        """
        Remove a product from the favorite list.
        """
        product_id = str(product.id)
        if product_id in self.favorite:
            del self.favorite[product_id]
            self.save()

    def get_total_retail_price_USD(self):
        return sum(Decimal(item['retail_price_USD']) * item['quantity'] for item in self.favorite.values())

    def clear(self):
        # remove favorite from session
        del self.session[settings.FAVORITER_SESSION_ID]
        self.save()

    def save(self):
        self.session.modified = True
