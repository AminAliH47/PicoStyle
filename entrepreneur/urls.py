from django.urls import path
from entrepreneur import views

app_name = "entrepreneur"

urlpatterns = (
    path('', views.EntrepreneursList.as_view(), name='list'),
    path('e/<int:pk>/', views.EntrepreneursDetail.as_view(), name='detail'),
)
