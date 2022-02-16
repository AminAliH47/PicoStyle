from django.urls import path
from favorite import views

app_name = 'favorite'

urlpatterns = (
    path('', views.favorite_detail, name='detail'),
    path('add/<int:product_id>/', views.favorite_add, name='add'),
    path('remove/<int:product_id>/', views.favorite_remove, name='remove'),
)
