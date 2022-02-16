from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_POST, require_GET

from extensions.extensions import grouper
from favorite.forms import FavoriteAddProductForm
from products import models
from products.filters import ProductFilter
from products.forms import ShowProductsForm, ProductsCategoryForm
from products.mixins import (FieldsMixin, FormValidMixin, SellerAccessMixin,
                             SuperuserAccessMixin, CategoryFormValidMixin, ShowProductFormValidMixin,
                             IncreaseFormValidMixin, IncreaseFieldsMixin, )

from products.models import (Products, ProductsCategory, ProductImages, PriceIncrease)
from django.shortcuts import (get_object_or_404, render)


# get category list for front end
class Node(dict):

    def __init__(self, uid, model):
        self._parent = None
        self['value'] = uid
        self['title'] = model.objects.get(id=uid).title
        self['child'] = []

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, node):
        self._parent = node
        node['child'].append(self)


def build(idPairs, model):
    lookup = {}
    for uid, pUID in idPairs:
        this = lookup.get(uid)
        if this is None:
            this = Node(uid, model)
            lookup[uid] = this

        if uid != pUID:
            parent = lookup[pUID]
            if not parent:
                parent = Node(pUID, model)
                lookup[pUID] = parent
            this.parent = parent
    return lookup


# Create your views here.

class ProductsList(generic.ListView):
    """view fo list of products"""
    template_name = 'products/pages/list.html'
    paginate_by = 9
    queryset = Products.objects.get_published_product()
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductsCategory.objects.filter(parent=None, active=True)
        return context


# @method_decorator([vary_on_cookie, cache_page(60 * 15)], name='dispatch')
class ProductsDetail(generic.DetailView):
    """view for detail Products"""
    model = Products
    context_object_name = "product"
    template_name = 'products/pages/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorite_form'] = FavoriteAddProductForm()

        product = kwargs['object']
        related_products = list(grouper(4, Products.objects.get_related_products(product=product)))
        context['related_products'] = related_products
        context['product_images'] = list(grouper(4, ProductImages.objects.filter(product=product)))
        return context


products = None
category = None


# @cache_page(60 * 15)
def category_list(request, item):
    """ View for products list by category """
    category_slugs = item.split('/')  # get parameter from url
    categories = []
    global products, category
    for slug in category_slugs:
        if not categories:
            parent = None
        else:
            parent = categories[-1]
        # get one category from url parameter
        category = get_object_or_404(ProductsCategory, slug=slug, parent=parent)

        # get published product from one category
        products = category.c_products.get_list()
        categories.append(category)

    parent = [cat for cat in categories][0]

    query = ProductFilter(request.GET, queryset=products)
    products = query.qs
    paginator = Paginator(products, 16)
    page = request.GET.get('page', 1)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,  # list of products in category
        'filter': query,  # list of products in category
        'cat': category,  # current category in url
        'parent': parent,  # parent category in url
        # 'categories': ProductsCategory.objects.filter(parent=None, active=True),
        'categories': categories,
        # 'h_categories': h_categories
    }
    return render(request, "products/pages/list.html", context)


class SearchProducts(generic.ListView):
    model = models.Products
    paginate_by = 16
    context_object_name = "products"
    template_name = "products/pages/search-list.html"

    def get_queryset(self):
        query = self.request.GET['q']
        return Products.objects.search_product(query)


def autocomplete_search(request):
    """ Product JSON list for autocomplete search """
    qs = Products.objects.get_published_product()
    # serialize queryset for transfer list to json
    data = serializers.serialize('json', queryset=qs, fields=('id', 'title', 'slug', 'category'))
    return JsonResponse(data, safe=False)


@require_POST
def remove_img(request):
    value = {
        'product_id': request.POST['product_id'],
        'id': request.POST['id'],
    }
    ProductImages.objects.filter(id=value['id'], product__id=value['product_id']).delete()
    return HttpResponse("OK")


# view for products
class CreateProducts(FieldsMixin, FormValidMixin, generic.CreateView):
    """view for create Products"""
    model = Products
    template_name = 'account/products/pages/create-update.html'
    success_url = reverse_lazy('account:p_list')

    def get_context_data(self, **kwargs):
        a = []
        for x in ProductsCategory.objects.all():
            if x.parent_id:
                a.append((x.id, x.parent_id))
            else:
                a.append((x.id, x.id))
        lookup = build(a, ProductsCategory)

        roots = [x for x in lookup.values() if x.parent is None]
        context = super().get_context_data(**kwargs)
        context['category'] = roots

        try:
            retail_percent = models.ProductPercent.objects.filter(slug__iexact="retailer")[0]
            context['retail_percent'] = retail_percent.value
        except IndexError:
            context['retail_percent'] = 100
        try:
            wholesale_percent = models.ProductPercent.objects.filter(slug__iexact="wholesale")[0]
            context['wholesale_percent'] = wholesale_percent.value
        except IndexError:
            context['wholesale_percent'] = 20

        return context


class UpdateProducts(FieldsMixin, FormValidMixin, SellerAccessMixin, generic.UpdateView):
    """view for update products"""
    model = Products
    template_name = 'account/products/pages/create-update.html'
    context_object_name = "product"
    success_url = reverse_lazy('account:p_list')

    def get_context_data(self, **kwargs):
        a = []
        for x in ProductsCategory.objects.all():
            if x.parent_id:
                a.append((x.id, x.parent_id))
            else:
                a.append((x.id, x.id))
        lookup = build(a, ProductsCategory)
        roots = [x for x in lookup.values() if x.parent is None]
        context = super().get_context_data(**kwargs)

        context['category'] = roots

        try:
            retail_percent = models.ProductPercent.objects.filter(slug__iexact="retailer")[0]
            context['retail_percent'] = retail_percent.value
        except IndexError:
            context['retail_percent'] = 100
        try:
            wholesale_percent = models.ProductPercent.objects.filter(slug__iexact="wholesale")[0]
            context['wholesale_percent'] = wholesale_percent.value
        except IndexError:
            context['wholesale_percent'] = 20

        return context


class DeleteProducts(SuperuserAccessMixin, generic.DeleteView):
    """view for delete products"""
    model = Products
    template_name = 'account/products/pages/delete.html'
    context_object_name = "product"

    def get_success_url(self):
        return self.request.GET['next']


# view for tag products
class CreateTag(SuperuserAccessMixin, generic.CreateView):
    """view for create Product tag"""
    model = models.ProductsTag
    fields = ('title',)
    template_name = ''
    context_object_name = "item"
    success_url = ''


class UpdateTag(SuperuserAccessMixin, generic.UpdateView):
    """view for update Product tag"""
    model = models.ProductsTag
    fields = ('title',)
    template_name = ''
    context_object_name = "item"
    success_url = ''


class DeleteTag(SuperuserAccessMixin, generic.DeleteView):
    """view for delete Product tag"""
    model = models.ProductsTag
    template_name = ''
    context_object_name = "item"
    success_url = ''


# view for ProductsType
class CreateType(SuperuserAccessMixin, generic.CreateView):
    """view for create Product type"""
    model = models.ProductsType
    fields = ('title',)
    template_name = ''
    context_object_name = "item"
    success_url = ''


class UpdateType(SuperuserAccessMixin, generic.UpdateView):
    """view for update Product type"""
    model = models.ProductsType
    fields = ('title',)
    template_name = ''
    context_object_name = "item"
    success_url = ''


class DeleteType(SuperuserAccessMixin, generic.DeleteView):
    """view for delete Product type"""
    model = models.ProductsType
    template_name = ''
    context_object_name = "item"
    success_url = ''


# view for Products category
class CreateCategory(SuperuserAccessMixin, CategoryFormValidMixin, generic.CreateView):
    """view for create Category"""
    model = models.ProductsCategory
    form_class = ProductsCategoryForm
    template_name = 'account/products/category/pages/create-update.html'
    context_object_name = "item"
    success_url = reverse_lazy("account:pc_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductsCategory.objects.all()
        return context


class UpdateCategory(SuperuserAccessMixin, CategoryFormValidMixin, generic.UpdateView):
    """view for update Category"""
    model = models.ProductsCategory
    form_class = ProductsCategoryForm
    template_name = 'account/products/category/pages/create-update.html'
    context_object_name = "item"

    def get_success_url(self):
        return self.request.GET['next']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductsCategory.objects.all()
        return context


class DeleteCategory(SuperuserAccessMixin, generic.DeleteView):
    """view for delete Category"""
    model = models.ProductsCategory
    template_name = 'account/items/pages/delete.html'
    context_object_name = "item"

    def get_success_url(self):
        return self.request.GET['next']


# view for ProductsMaterial
class CreateMaterial(SuperuserAccessMixin, generic.CreateView):
    """view for create Material"""
    model = models.ProductMaterial
    fields = ('title',)
    template_name = ''
    context_object_name = "item"
    success_url = ''


class UpdateMaterial(SuperuserAccessMixin, generic.UpdateView):
    """view for update Material"""
    model = models.ProductMaterial
    fields = ('title',)
    template_name = ''
    context_object_name = "item"
    success_url = ''


class DeleteMaterial(SuperuserAccessMixin, generic.DeleteView):
    """view for delete Material"""
    model = models.ProductMaterial
    template_name = ''
    context_object_name = "item"
    success_url = ''


# view for Shoe sole
class CreateShoeSole(SuperuserAccessMixin, generic.CreateView):
    """view for create Shoe sole"""
    model = models.ShoeSole
    fields = ('title',)
    template_name = ''
    context_object_name = "item"
    success_url = ''


class UpdateShoeSole(SuperuserAccessMixin, generic.UpdateView):
    """view for update Shoe sole"""
    model = models.ShoeSole
    fields = ('title',)
    template_name = ''
    context_object_name = "item"
    success_url = ''


class DeleteShoeSole(SuperuserAccessMixin, generic.DeleteView):
    """view for delete Shoe sole"""
    model = models.ShoeSole
    context_object_name = "item"
    template_name = ''
    success_url = ''


class UpdateProductPercent(SuperuserAccessMixin, generic.UpdateView):
    """view for update product price percent"""
    model = models.ProductPercent
    fields = ('value',)
    context_object_name = "item"
    template_name = "account/items/pages/create-update.html"
    success_url = reverse_lazy("account:ppp_list")


@require_GET
def size_list(request):
    sizes = serializers.serialize('json', queryset=models.ProductSize.objects.all(), fields=('id', 'title',))
    return HttpResponse(sizes, 'application/json')


@require_POST
def create_size(request):
    title = request.POST.get('title')
    models.ProductSize.objects.get_or_create(title=title)
    sizes = serializers.serialize('json', queryset=models.ProductSize.objects.all(), fields=('title',))
    return HttpResponse(sizes, 'application/json')


# view for Product show/hide
class CreateShow(SuperuserAccessMixin, ShowProductFormValidMixin, generic.CreateView):
    """view for create Product show/hide status"""
    model = models.ShowProducts
    form_class = ShowProductsForm
    template_name = 'account/products/show/pages/create-update.html'
    success_url = reverse_lazy("account:ps_list")


class UpdateShow(SuperuserAccessMixin, ShowProductFormValidMixin, generic.UpdateView):
    """view for update Product show/hide status"""
    model = models.ShowProducts
    form_class = ShowProductsForm
    template_name = 'account/products/show/pages/create-update.html'
    context_object_name = "item"
    success_url = reverse_lazy("account:ps_list")


class DeleteShow(SuperuserAccessMixin, generic.DeleteView):
    """view for delete Product show/hide status"""
    model = models.ShowProducts
    template_name = 'account/items/pages/delete.html'
    context_object_name = "item"
    success_url = reverse_lazy("account:ps_list")


class CreateIncrease(IncreaseFormValidMixin, IncreaseFieldsMixin, generic.CreateView):
    """ view for create product increase """
    model = PriceIncrease
    template_name = 'account/products/increase/pages/create-update.html'
    success_url = reverse_lazy("account:pi_list")

    def get_form_kwargs(self):
        """ Pass user from request to model form """
        kwargs = super(CreateIncrease, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class UpdateIncrease(IncreaseFormValidMixin, IncreaseFieldsMixin, generic.UpdateView):
    """ view for update product increase """
    model = PriceIncrease
    context_object_name = "increase"
    template_name = 'account/products/increase/pages/create-update.html'
    success_url = reverse_lazy("account:pi_list")

    def get_form_kwargs(self):
        """ Pass user from request to model form """
        kwargs = super(UpdateIncrease, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class DeleteIncrease(SuperuserAccessMixin, generic.DeleteView):
    """ view for delete product increase """
    model = PriceIncrease
    context_object_name = "item"
    template_name = 'account/items/pages/delete.html'
    success_url = reverse_lazy("account:pi_list")

    # def delete(self, request, *args, **kwargs):
    #     item = Discounts.objects.get(pk=self.kwargs['pk'])
    #     all_products = item.all_products
    #     seller = item.seller
    #
    #     ws_p = ProductPercent.objects.filter(slug__iexact="wholesale")[0]
    #     r_p = ProductPercent.objects.filter(slug__iexact="retailer")[0]
    #
    #     wholesale_discount = 0
    #     retail_discount = 0
    #
    #     if all_products:
    #         query = Products.objects.filter(seller=seller)
    #     else:
    #         category = item.category
    #         query = Products.objects.filter(category=category).filter(seller=seller)
    #
    #     for product in query:
    #         product.wholesale_discount = wholesale_discount
    #         product.retail_discount = retail_discount
    #         product.wholesale_price = f"{cal_wholesale_price(product, wholesale_discount, ws_p)} $"
    #         product.retail_price_USD = f"{cal_retail_price(r_p, retail_discount)} $"
    #     Products.objects.bulk_update(query,
    #                                  fields=['wholesale_discount', 'retail_discount', 'wholesale_price',
    #                                          'retail_price_USD'])
    #     return super(DeleteDiscounts, self).delete(request)
