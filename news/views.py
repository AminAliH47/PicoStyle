from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from news.models import (
    News,
    CategoryNews,
)
from news.mixins import (
    FieldsMixin,
    FormValidMixin,
    AuthorAccessMixin,
    SuperuserAccessMixin,
)
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy


# view for show of news
@method_decorator([vary_on_cookie, cache_page(60 * 30)], name='dispatch')
class NewsList(generic.ListView):
    """
    List of news
    """
    template_name = 'news/pages/list.html'
    paginate_by = 9
    context_object_name = "news"
    queryset = News.objects.get_published_news()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = CategoryNews.objects.get_active_category()
        return context


category = None


@method_decorator([vary_on_cookie, cache_page(60 * 30)], name='dispatch')
class CategoryList(generic.ListView):
    """
    List of news in category
    """
    context_object_name = "news"
    template_name = 'news/pages/list.html'
    paginate_by = 9

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(CategoryNews.objects.get_active_category(), slug=slug)
        return category.news.get_published_news()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        context['categories'] = CategoryNews.objects.get_active_category()
        return context


class NewsDetail(generic.DetailView):
    """
    Detail of News
    """
    queryset = News.objects.get_published_news()
    template_name = 'news/pages/detail.html'


# view for create new news
class CreateNews(FieldsMixin, FormValidMixin, LoginRequiredMixin, generic.CreateView):
    """
    Create news in admin panel
    """
    model = News
    template_name = 'account/news/pages/create-update.html'
    success_url = reverse_lazy("account:n_list")


class UpdateNews(FieldsMixin, FormValidMixin, AuthorAccessMixin, generic.UpdateView):
    """
    Update news in admin panel
    """
    model = News
    context_object_name = "news"
    template_name = 'account/news/pages/create-update.html'
    success_url = reverse_lazy("account:n_list")


class DeleteNews(SuperuserAccessMixin, generic.DeleteView):
    """
    Delete news in admin panel
    """
    model = News
    template_name = 'account/news/pages/delete.html'
    context_object_name = "news"
    success_url = reverse_lazy('account:n_list')


# view for create new news
class CreateNewsCategory(SuperuserAccessMixin, generic.CreateView):
    """
    Create news category in admin panel
    """
    model = CategoryNews
    fields = ('title', 'image', 'icon', 'active',)
    template_name = 'account/news/category/pages/create-update.html'
    success_url = reverse_lazy("account:nc_list")


class UpdateNewsCategory(SuperuserAccessMixin, generic.UpdateView):
    """
    Update news category in admin panel
    """
    model = CategoryNews
    fields = ('title', 'image', 'icon', 'active',)
    context_object_name = "item"
    template_name = 'account/news/category/pages/create-update.html'
    success_url = reverse_lazy("account:nc_list")


class DeleteNewsCategory(SuperuserAccessMixin, generic.DeleteView):
    """
    Delete news category in admin panel
    """
    model = CategoryNews
    context_object_name = "item"
    template_name = 'account/items/pages/delete.html'
    success_url = reverse_lazy('account:nc_list')
