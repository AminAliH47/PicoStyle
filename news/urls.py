from django.urls import path
from news import views

app_name = "news"

urlpatterns = (
    path('', views.NewsList.as_view(), name='list'),
    path('<int:pk>/<slug:slug>', views.NewsDetail.as_view(), name='detail'),
    path('category/<slug:slug>/', views.CategoryList.as_view(), name='category'),
)
