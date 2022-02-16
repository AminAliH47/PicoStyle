from django.contrib import (
    auth,
    messages,
)
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import (
    render,
    redirect,
)
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from account.forms import (
    LoginUserForm,
    PasswordForm,
)
from account.models import User
from discount.models import (
    Discounts,
    ShowDiscount,
)
from extensions.extensions import grouper
from messages.models import Messages
from news.models import News, CategoryNews
from pages.models import Pages
from products.filters import (
    ProductPanelFilter,
    CategoryPanelFilter,
)
from products.models import (
    Products,
    ProductsCategory,
    ProductImages,
    ProductPercent,
    ShowProducts,
    PriceIncrease,
)
from django.shortcuts import get_object_or_404
from news.mixins import (
    AuthorAccessMixin,
    SuperuserAccessMixin,
)
from account.mixins import (
    FieldsUserMixin,
    SellerFormValidMixin,
    FieldsSellerMixin,
    SellerAccountAccessMixin,
    UpdateFieldsSellerMixin,
    UpdateSellerFormValidMixin
)
from products.mixins import SellerAccessMixin
from main import models as m_models


class Index(LoginRequiredMixin, generic.TemplateView):
    """
    Admin panel main page (index)
    """
    template_name = 'account/pages/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['seller_count'] = User.objects.seller_count(),
        context['product_count'] = Products.objects.product_count(),
        context['category_count'] = ProductsCategory.objects.category_count(),
        return context


def login(request):
    redirect_to = request.GET['next']  # get url to redirect user after login
    form = LoginUserForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user_input = form.cleaned_data['username']
            # check user enter email or username
            try:
                username = User.objects.get(email=user_input).username
            except User.DoesNotExist:
                username = user_input
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect(redirect_to)
            else:
                messages.error(request, _("The username or password entered is incorrect"))
        else:
            messages.error(request, _("The username or password entered is incorrect"))

    context = {
        "form": form
    }
    return render(request, "account/pages/login.html", context)


def logout(request):
    auth.logout(request)
    return redirect(reverse_lazy("main:index"))


@method_decorator([vary_on_cookie, cache_page(60 * 15)], name='dispatch')
class SellerPanelList(SuperuserAccessMixin, generic.ListView):
    """
    List of Seller users
    """
    model = User
    queryset = User.objects.get_sellers()
    paginate_by = 10
    context_object_name = "sellers"
    template_name = 'account/seller/pages/list.html'


@method_decorator([vary_on_cookie, cache_page(60 * 30)], name='dispatch')
class SellerPanelDetail(SellerAccountAccessMixin, generic.DetailView):
    """
    Seller detail panel
    """
    model = User
    context_object_name = "seller"
    template_name = 'account/seller/pages/detail.html'


class CreateSeller(SuperuserAccessMixin, SellerFormValidMixin, FieldsSellerMixin, generic.CreateView):
    """
    Create seller user
    """
    model = User
    template_name = 'account/seller/pages/create-update.html'
    success_url = reverse_lazy("account:s_list")


class UpdateSeller(SellerAccountAccessMixin, UpdateSellerFormValidMixin, UpdateFieldsSellerMixin, generic.UpdateView):
    """
    Update seller user
    """
    model = User
    context_object_name = "seller"
    template_name = 'account/seller/pages/create-update.html'

    def get_success_url(self):
        return self.request.GET['next']


class DeleteSeller(SuperuserAccessMixin, generic.DeleteView):
    """
    Delete Seller user
    """
    model = User
    context_object_name = "seller"
    template_name = 'account/seller/pages/delete.html'

    def get_success_url(self):
        return self.request.GET['next']


def change_password(request, pk):
    form = PasswordForm(request.POST or None)
    user = get_object_or_404(User, pk=pk)

    if request.method == "POST" and form.is_valid():
        password = form.cleaned_data['password']
        re_password = form.cleaned_data['re_password']
        if password == re_password:
            user.password = make_password(password)
            user.save()
            return redirect("account:index")
        else:
            messages.error(request, _("Password and Confirm password are different"))
    context = {
        "form": form,
        "user": user,
    }
    if request.user.is_superuser or request.user == user:
        return render(request, "account/pages/change_password.html", context)
    else:
        raise Http404()


# view for news app
class NewsPanelList(generic.ListView):
    """
    List of news in admin panel
    """
    paginate_by = 10
    template_name = "account/news/pages/list.html"
    context_object_name = "news"

    def get_queryset(self):
        if self.request.user.is_anonymous:
            raise Http404
        elif self.request.user.is_superuser:  # check user if superuser can see all news
            return News.objects.all()
        elif self.request.user.is_author:
            return News.objects.filter(
                author=self.request.user)  # check user if not superuser can see self news
        else:
            raise Http404()


class PreviewNews(AuthorAccessMixin, generic.DetailView):
    """
    Preview News in admin panel
    """
    template_name = "account/news/pages/preview.html"
    context_object_name = "news"

    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')
        return get_object_or_404(News, pk=pk)


superuser_products = None
seller_products = None


# views for products app
class ProductPanelList(generic.ListView):
    """
    List of products in admin panel
    """
    template_name = "account/products/pages/list.html"
    context_object_name = "products"
    paginate_by = 20

    def get_queryset(self):
        global superuser_products, seller_products

        superuser_products = ProductPanelFilter(self.request.GET, queryset=Products.objects.all())
        seller_products = ProductPanelFilter(self.request.GET, queryset=Products.objects.filter(
            seller=self.request.user))
        if self.request.user.is_anonymous:
            raise Http404
        elif self.request.user.is_superuser:  # check if user is superuser can see all products
            return superuser_products.qs
        elif self.request.user.is_seller:
            return seller_products.qs  # check if user is seller can see self products
        else:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super(ProductPanelList, self).get_context_data(**kwargs)
        if self.request.user.is_superuser:
            context['filter'] = superuser_products
        elif self.request.user.is_seller:
            context['filter'] = seller_products
        return context


categories = None


class ProductCategoryList(SuperuserAccessMixin, generic.ListView):
    """
    List of products category in admin panel
    """
    model = ProductsCategory
    paginate_by = 20
    context_object_name = "categories"
    template_name = "account/products/category/pages/list.html"

    def get_queryset(self):
        global categories
        categories = CategoryPanelFilter(self.request.GET, queryset=ProductsCategory.objects.all())
        return categories.qs

    def get_context_data(self, **kwargs):
        context = super(ProductCategoryList, self).get_context_data(**kwargs)
        context['filter'] = categories
        return context


@method_decorator([vary_on_cookie, cache_page(60 * 15)], name='dispatch')
class PreviewProduct(SellerAccessMixin, generic.DetailView):
    """
    view for preview Product in admin panel
    """
    template_name = "account/products/pages/preview.html"
    context_object_name = "product"

    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Products, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = kwargs['object']
        related_products = list(grouper(4, Products.objects.get_related_products(product=product)))
        context['related_products'] = related_products
        context['product_images'] = list(grouper(4, ProductImages.objects.filter(product=product)))
        return context


class ProductPercentList(SuperuserAccessMixin, generic.ListView):
    """
    Product dynamic price percentage list in admin
    """
    model = ProductPercent
    context_object_name = "items"
    template_name = "account/products/percent/pages/list.html"


class ManagePriceList(SuperuserAccessMixin, generic.TemplateView):
    """
    Manage price view in admin panel
    """
    template_name = "account/products/price/pages/main-list.html"


# view for brands app
class BrandsPanelList(SuperuserAccessMixin, generic.ListView):
    """
    List of brands in admin panel
    """
    queryset = User.objects.filter(is_brand=True)
    context_object_name = "brands"
    template_name = "account/brands/pages/list.html"


class PreviewBrands(SuperuserAccessMixin, generic.DetailView):
    """
    Preview brands in admin panel
    """
    template_name = "account/brand/pages/preview.html"
    context_object_name = "brand"

    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')
        return get_object_or_404(User, pk=pk)


# Site Items sections
class ItemsList(generic.TemplateView):
    """
    Site setting and configuration view in admin panel
    """
    template_name = "account/items/pages/main-list.html"


# views for main app
class MainSliderList(SuperuserAccessMixin, generic.ListView):
    """
    List of main slider in admin panel
    """
    template_name = "account/items/pages/list.html"
    context_object_name = "items"
    queryset = m_models.MainSlider.objects.all()


class BrandsSliderList(SuperuserAccessMixin, generic.ListView):
    """
    List of brands slider in admin panel
    """
    template_name = "account/items/pages/list.html"
    context_object_name = "items"
    queryset = m_models.BrandsSlider.objects.all()


class MainCategoriesList(SuperuserAccessMixin, generic.ListView):
    """
    List of main categories (category image in index page) in admin panel
    """
    template_name = "account/items/pages/list.html"
    context_object_name = "items"
    queryset = m_models.MainCategories.objects.all()


class SocialMediaList(SuperuserAccessMixin, generic.ListView):
    """
    List of social media in admin panel
    """
    template_name = "account/items/pages/list.html"
    context_object_name = "items"
    queryset = m_models.SocialMedia.objects.all()


class SpecialProjectsList(SuperuserAccessMixin, generic.ListView):
    """
    List of special projects in admin panel
    """
    template_name = "account/items/pages/list.html"
    context_object_name = "items"
    queryset = m_models.SpecialProjects.objects.all()


class WorkWithUsList(SuperuserAccessMixin, generic.ListView):
    """
    List of work with us in admin panel
    """
    template_name = "account/items/pages/list.html"
    context_object_name = "items"
    queryset = m_models.WorkWithUs.objects.all()


class StoreAgentList(SuperuserAccessMixin, generic.ListView):
    """
    List of store and agent in admin panel
    """
    template_name = "account/store_agent/pages/list.html"
    context_object_name = "items"
    queryset = m_models.StoreAgent.objects.all()


class SizeGuideList(SuperuserAccessMixin, generic.ListView):
    """
    List of size guide in admin panel
    """
    template_name = "account/items/pages/list.html"
    context_object_name = "items"
    queryset = m_models.SizeGuide.objects.all()


class PagesList(SuperuserAccessMixin, generic.ListView):
    """
    List of pages in admin panel
    """
    template_name = "account/items/pages/list.html"
    context_object_name = "items"
    queryset = Pages.objects.all()


@method_decorator([vary_on_cookie, cache_page(60 * 5)], name='dispatch')
class MessagesList(generic.ListView):
    """
    List of messages in admin panel
    """
    paginate_by = 10
    template_name = "account/messages/pages/list.html"
    context_object_name = "messages"

    def get_queryset(self):
        if self.request.user.is_anonymous:
            raise Http404
        elif self.request.user.is_superuser:
            return Messages.objects.all()
        elif self.request.user.is_seller:
            return Messages.objects.filter(seller=self.request.user)
        else:
            raise Http404


class MessagesDetail(generic.DetailView):
    """
    Detail of messages in admin panel
    """
    template_name = "account/messages/pages/detail.html"
    context_object_name = "message"

    def get_object(self, queryset=None):
        message = Messages.objects.get(pk=self.kwargs['pk'])
        if self.request.user.is_anonymous:
            raise Http404
        elif self.request.user.is_superuser:
            if message.seller.pk == self.request.user.pk:  # Change message read status
                message.is_read = True
                message.save()
            return get_object_or_404(Messages, pk=self.kwargs['pk'])
        elif self.request.user.is_seller:
            if message.seller.pk == self.request.user.pk:  # Change message read status
                message.is_read = True
                message.save()
            return get_object_or_404(Messages, pk=self.kwargs['pk'], seller=self.request.user)
        else:
            raise Http404


class DiscountList(generic.ListView):
    """
    List of product discount in admin panel
    """
    paginate_by = 10
    template_name = "account/discount/pages/list.html"
    context_object_name = "discounts"

    def get_queryset(self):
        if self.request.user.is_anonymous:
            raise Http404
        elif self.request.user.is_superuser:  # check user if superuser can see all discounts
            return Discounts.objects.all()
        elif self.request.user.is_seller:
            return Discounts.objects.filter(
                seller=self.request.user)  # check user if not superuser can see self discounts
        else:
            raise Http404


class IncreaseList(generic.ListView):
    """
    List of product price increase in admin panel
    """
    paginate_by = 10
    template_name = "account/products/increase/pages/list.html"
    context_object_name = "increases"

    def get_queryset(self):
        if self.request.user.is_anonymous:
            raise Http404
        elif self.request.user.is_superuser:  # check user if superuser can see all discounts
            return PriceIncrease.objects.all()
        elif self.request.user.is_seller:
            return PriceIncrease.objects.filter(
                seller=self.request.user)  # check user if not superuser can see self discounts
        else:
            raise Http404


class NewsCategoryList(SuperuserAccessMixin, generic.ListView):
    """
    List of news category in admin panel
    """
    model = CategoryNews
    context_object_name = "categories"
    template_name = "account/news/category/pages/list.html"


class ShowProductsList(SuperuserAccessMixin, generic.ListView):
    """
    List of product show/hide status in admin panel
    """
    model = ShowProducts
    context_object_name = "items"
    template_name = "account/products/show/pages/list.html"


class ShowDiscountList(SuperuserAccessMixin, generic.ListView):
    """
    List of discount show/hide status in admin panel
    """
    model = ShowDiscount
    context_object_name = "items"
    template_name = "account/discount/show/pages/list.html"
