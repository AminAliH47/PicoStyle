from random import randint

from django.db import InternalError
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from extensions.extensions import inactivate_status, cal_wholesale_price2, cal_retail_price2
from products.models import (Products, ProductsCategory, ProductsTag, ProductImages, ProductPercent)


# mixin for products
class FieldsMixin:
    """mixin for show filed filter in superuser and author"""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            raise Http404
        elif request.user.is_superuser:
            from products.forms import ProductSuperuserForm  # Import locally
            self.form_class = ProductSuperuserForm
        elif request.user.is_seller:
            from products.forms import ProductSellerForm  # Import locally
            self.form_class = ProductSellerForm
        else:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class FormValidMixin:
    """mixin for show form """

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            self.obj = form.save(commit=False)
            self.obj.seller = self.request.user
            self.obj.status = 'pending'
        obj = form.save(commit=False)
        obj.save()
        form.save_m2m()

        obj.type = [x.title for x in obj.all_categories][1]
        obj.wholesale_price = self.request.POST['name_wPrice']
        obj.retail_price_USD = self.request.POST['name_rPrice']

        if not obj.code2:
            code = f"{obj.seller.id}{[x.title for x in obj.all_categories][-1][0]}{obj.type[0]}{randint(1000, 9999)}"
            try:
                obj.code2 = code
            except InternalError as e:
                if 'unique constraint' in e.message:
                    code = f"{obj.seller.id}{[x.title for x in obj.all_categories][-1][0]}{obj.type[0]}{randint(1000, 9999)}"
                    obj.code2 = code

        obj.save()

        for x in obj.all_categories:
            category = ProductsCategory.objects.get(id=x.id)
            if category not in obj.category.all():
                obj.category.add(category)

        images = self.request.FILES.getlist('images[]')

        # Saving the images
        for img in images:
            ProductImages(image=img, product=obj).save()

        try:
            url_next = self.request.GET['next']
        except:
            url_next = None

        if url_next:
            return HttpResponseRedirect(url_next)
        else:
            from django.urls import reverse_lazy
            return HttpResponseRedirect(reverse_lazy("account:p_list"))


class CategoryFormValidMixin:
    """mixin for show form """

    def form_valid(self, form):
        self.obj = form.save(commit=False)
        category = self.obj
        self.obj.save()
        if category.children.all():
            if not category.active:
                categories = category.children.all()
                for cat in categories:
                    cat.active = False
                    if cat.children.all():
                        inactivate_status(cat, ProductsCategory)
                ProductsCategory.objects.bulk_update(categories, fields=['active'])

        if category.parent:
            if category.active:
                categories = category.all_parent
                for cat in categories:
                    cat.active = True
                ProductsCategory.objects.bulk_update(categories, fields=['active'])

        return super(CategoryFormValidMixin, self).form_valid(form)


class SuperuserAccessMixin:
    """mixin for check is superuser for delete products"""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404


# mixin tag products
class FieldsMixinTag:
    """mixin for show filed tag to superuser"""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            raise Http404
        elif request.user.is_superuser:
            from products.forms import ProductsTagForm  # Import locally
            self.form_class = ProductsTagForm
        elif request.user.is_seller:
            from products.forms import ProductsTagForm  # Import locally
            self.form_class = ProductsTagForm
        else:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class AuthorAccessMixin:
    """mixin for check AuthorAccess"""

    def dispatch(self, request, pk, *args, **kwargs):
        tag = get_object_or_404(ProductsTag, pk=pk)
        if tag.author == request.user or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404


# mixin type products
class FieldsMixinType:
    """mixin for show filed type to superuser"""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            raise Http404
        elif request.user.is_superuser:
            from products.forms import ProductsTypeForm  # Import locally
            self.form_class = ProductsTypeForm
        elif request.user.is_seller:
            from products.forms import ProductsTypeForm  # Import locally
            self.form_class = ProductsTypeForm
        else:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


# mixin category products
class FieldsMixinCategory:

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            raise Http404
        elif request.user.is_superuser:
            from products.forms import ProductsCategoryForm  # Import locally
            self.form_class = ProductsCategoryForm
        elif request.user.is_seller:
            from products.forms import ProductsCategoryForm  # Import locally
            self.form_class = ProductsCategoryForm
        else:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


# mixin ProductsMaterial
class FieldsMixinProductsMaterial:

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            raise Http404
        elif request.user.is_superuser:
            from products.forms import ProductsMaterialForm  # Import locally
            self.form_class = ProductsMaterialForm
        elif request.user.is_seller:
            from products.forms import ProductsMaterialForm  # Import locally
            self.form_class = ProductsMaterialForm
        else:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


# mixin ShoeSole
class FieldsMixinShoeSole:

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            raise Http404
        elif request.user.is_superuser:
            from products.forms import ProductsShoeSoleForm  # Import locally
            self.form_class = ProductsShoeSoleForm
        elif request.user.is_seller:
            from products.forms import ProductsShoeSoleForm  # Import locally
            self.form_class = ProductsShoeSoleForm
        else:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class SellerAccessMixin:
    """mixin for check SellerAccess"""

    def dispatch(self, request, *args, **kwargs):
        product = get_object_or_404(Products, pk=kwargs.get('pk'))
        if product.seller == request.user or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404


class ShowProductFormValidMixin:
    def form_valid(self, form):
        self.obj = form.save(commit=False)
        category = form.cleaned_data['category']
        brand = form.cleaned_data['brand']
        show_retail_price = form.cleaned_data['show_retail_price']
        show_wholesale_price = form.cleaned_data['show_wholesale_price']
        if category:
            products = Products.objects.filter(category=category)
            for product in products:
                product.show_retail_price = show_retail_price
                product.show_wholesale_price = show_wholesale_price
            Products.objects.bulk_update(products, fields=['show_retail_price', 'show_wholesale_price'])
        if brand:
            products = Products.objects.filter(seller=brand)
            for product in products:
                product.show_retail_price = show_retail_price
                product.show_wholesale_price = show_wholesale_price
            Products.objects.bulk_update(products, fields=['show_retail_price', 'show_wholesale_price'])

        return super(ShowProductFormValidMixin, self).form_valid(form)


class IncreaseFieldsMixin:
    """mixin for show filed filter in superuser and seller"""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            from products.forms import IncreaseFormSuperuser  # Import Locally
            self.form_class = IncreaseFormSuperuser
        elif request.user.is_seller:
            from products.forms import IncreaseFormSeller  # Import Locally
            self.form_class = IncreaseFormSeller
        else:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class IncreaseFormValidMixin:
    """ mixin To increase the price """

    def form_valid(self, form):
        if self.request.user.is_superuser:
            status = form.cleaned_data['status']
            all_products = form.cleaned_data['all_products']
            seller = form.cleaned_data['seller']

            ws_p = ProductPercent.objects.filter(slug__iexact="wholesale")[0]
            r_p = ProductPercent.objects.filter(slug__iexact="retailer")[0]

            if status == "accepted":
                value = form.cleaned_data['value']

                if all_products:
                    query = Products.objects.filter(seller=seller)
                else:
                    category = form.cleaned_data['category']
                    query = Products.objects.filter(category=category).filter(seller=seller)

                for product in query:
                    price_value = value + int(product.exw_price.replace(",", ""))
                    product.exw_price = price_value
                    product.wholesale_price = f"{cal_wholesale_price2(product, price_value, ws_p)} $"
                    product.retail_price_USD = f"{cal_retail_price2(r_p, product)} $"
                # Products.objects.bulk_update(query,
                #                              fields=['exw_price', 'wholesale_price',
                #                                      'retail_price_USD'])
        else:
            self.obj = form.seve(commit=False)
            self.obj.seller = self.request.user
            self.obj.status = 'pending'
        return super().form_valid(form)
