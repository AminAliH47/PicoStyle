from django.shortcuts import (render, get_object_or_404, redirect, )

# Create your views here.
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from favorite.favorite import Favorite
from favorite.forms import FavoriteAddProductForm
from products.models import Products


@require_POST
def favorite_add(request, product_id):
    favorite = Favorite(request)
    product = get_object_or_404(Products, id=product_id)
    form = FavoriteAddProductForm(request.POST)
    if form.is_valid():
        favorite.add(product=product,
                     quantity=1,
                     override_quantity=form.cleaned_data['override'])
    return redirect(reverse_lazy('favorite:detail'))


@require_POST
def favorite_remove(request, product_id):
    favorite = Favorite(request)
    product = get_object_or_404(Products, id=product_id)
    favorite.remove(product)
    return redirect(reverse_lazy('favorite:detail'))


def favorite_detail(request):
    favorite = Favorite(request)
    return render(request, 'favorite/pages/detail.html', {'favorite': favorite})
