from django.http import Http404

from extensions.extensions import cal_wholesale_price, cal_retail_price
from products.models import Products, ProductPercent


class FieldsMixin:
    """mixin for show filed filter in superuser and author"""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            from discount.forms import DiscountsFormSuperuser  # Import Locally
            self.form_class = DiscountsFormSuperuser
        elif request.user.is_seller:
            from discount.forms import DiscountsFormSeller  # Import Locally
            self.form_class = DiscountsFormSeller
        else:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class FormValidMixin:
    """ mixin To apply a discount on the price """

    def form_valid(self, form):
        if self.request.user.is_superuser:
            status = form.cleaned_data['status']
            all_products = form.cleaned_data['all_products']
            seller = form.cleaned_data['seller']

            ws_p = ProductPercent.objects.filter(slug__iexact="wholesale")[0]
            r_p = ProductPercent.objects.filter(slug__iexact="retailer")[0]

            if status == "accepted":
                wholesale_discount = form.cleaned_data['wholesale_value']
                retail_discount = form.cleaned_data['retail_value']
            elif status == "rejected":
                wholesale_discount = 0
                retail_discount = 0
            else:
                form.save()
                return super().form_valid(form)

            if all_products:
                query = Products.objects.filter(seller=seller)
            else:
                category = form.cleaned_data['category']
                query = Products.objects.filter(category=category).filter(seller=seller)

            for product in query:
                product.wholesale_discount = wholesale_discount
                product.retail_discount = retail_discount
                product.wholesale_price = f"{cal_wholesale_price(product, wholesale_discount, ws_p)} $"
                product.retail_price_USD = f"{cal_retail_price(r_p, retail_discount)} $"
            Products.objects.bulk_update(query,
                                         fields=['wholesale_discount', 'retail_discount', 'wholesale_price',
                                                 'retail_price_USD'])
        else:
            self.obj = form.seve(commit=False)
            self.obj.seller = self.request.user
            self.obj.status = 'pending'
        return super().form_valid(form)


class ShowDiscountFormValidMixin:
    def form_valid(self, form):
        self.obj = form.save(commit=False)
        category = form.cleaned_data['category']
        brand = form.cleaned_data['brand']
        show_discount = form.cleaned_data['show_discount']
        if category:
            products = Products.objects.filter(category=category)
            for product in products:
                product.show_discount = show_discount
            Products.objects.bulk_update(products, fields=['show_discount'])
        if brand:
            products = Products.objects.filter(seller=brand)
            for product in products:
                product.show_discount = show_discount
            Products.objects.bulk_update(products, fields=['show_discount'])

        return super(ShowDiscountFormValidMixin, self).form_valid(form)
