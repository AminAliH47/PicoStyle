from django.urls import path
from brands import views

app_name = "brands"

urlpatterns = (
    path('', views.BrandsList.as_view(), name='list'),
    path('<int:pk>/', views.BrandsDetail.as_view(), name='detail'),
)
