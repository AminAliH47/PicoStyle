from django.urls import reverse_lazy
from django.views import generic
from discount.forms import ShowDiscountForm
from discount.mixins import ShowDiscountFormValidMixin
from discount.models import (
    Discounts,
    ShowDiscount,
)
from extensions.extensions import (
    cal_wholesale_price,
    cal_retail_price,
)
from products.mixins import SuperuserAccessMixin
from discount import mixins
from products.models import (
    ProductPercent,
    Products,
)


class CreateDiscounts(mixins.FormValidMixin, mixins.FieldsMixin, generic.CreateView):
    """
    Create Discounts in admin panel
    """
    model = Discounts
    template_name = 'account/discount/pages/create-update.html'
    success_url = reverse_lazy("account:d_list")

    def get_form_kwargs(self):
        """ Pass user from request to model form """
        kwargs = super(CreateDiscounts, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class UpdateDiscounts(mixins.FormValidMixin, mixins.FieldsMixin, generic.UpdateView):
    """
    Update Discounts
    """
    model = Discounts
    context_object_name = "discount"
    template_name = 'account/discount/pages/create-update.html'
    success_url = reverse_lazy("account:d_list")

    def get_form_kwargs(self):
        """ Pass user from request to model form """
        kwargs = super(UpdateDiscounts, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class DeleteDiscounts(SuperuserAccessMixin, generic.DeleteView):
    """
    Delete Discounts in admin panel
    """
    model = Discounts
    context_object_name = "item"
    template_name = 'account/items/pages/delete.html'
    success_url = reverse_lazy("account:d_list")

    def delete(self, request, *args, **kwargs):
        item = Discounts.objects.get(pk=self.kwargs['pk'])
        all_products = item.all_products
        seller = item.seller

        ws_p = ProductPercent.objects.filter(slug__iexact="wholesale")[0]
        r_p = ProductPercent.objects.filter(slug__iexact="retailer")[0]

        wholesale_discount = 0
        retail_discount = 0

        if all_products:
            query = Products.objects.filter(seller=seller)
        else:
            category = item.category
            query = Products.objects.filter(category=category).filter(seller=seller)

        for product in query:
            product.wholesale_discount = wholesale_discount
            product.retail_discount = retail_discount
            product.wholesale_price = f"{cal_wholesale_price(product, wholesale_discount, ws_p)} $"
            product.retail_price_USD = f"{cal_retail_price(r_p, retail_discount)} $"
        Products.objects.bulk_update(query,
                                     fields=['wholesale_discount', 'retail_discount', 'wholesale_price',
                                             'retail_price_USD'])
        return super(DeleteDiscounts, self).delete(request)


# view for Discount show/hide
class CreateShow(SuperuserAccessMixin, ShowDiscountFormValidMixin, generic.CreateView):
    """
    Create Discount show/hide status in admin panel
    """
    model = ShowDiscount
    form_class = ShowDiscountForm
    template_name = 'account/discount/show/pages/create-update.html'
    success_url = reverse_lazy("account:ds_list")


class UpdateShow(SuperuserAccessMixin, ShowDiscountFormValidMixin, generic.UpdateView):
    """
    Update Discount show/hide status in admin panel
    """
    model = ShowDiscount
    form_class = ShowDiscountForm
    template_name = 'account/discount/show/pages/create-update.html'
    context_object_name = "item"
    success_url = reverse_lazy("account:ds_list")


class DeleteShow(SuperuserAccessMixin, generic.DeleteView):
    """
    Delete Discount show/hide status in admin panel
    """
    model = ShowDiscount
    template_name = 'account/items/pages/delete.html'
    context_object_name = "item"
    success_url = reverse_lazy("account:ds_list")
