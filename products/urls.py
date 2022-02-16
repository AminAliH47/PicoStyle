from django.urls import path
from products import views

app_name = "products"

urlpatterns = (
    path('search', views.SearchProducts.as_view(), name="search"),
    path('autocomplete', views.autocomplete_search, name="autocomplete"),
    path('remove-img/', views.remove_img, name="remove_img"),
    # Size section
    path('size-list/', views.size_list, name="size_list"),
    path('create-size/', views.create_size, name="create_size"),
    path('d/<int:pk>/', views.ProductsDetail.as_view(), name="detail"),
    path('<path:item>', views.category_list, name="p_category"),
)
