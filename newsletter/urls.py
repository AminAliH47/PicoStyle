from django.urls import path
from newsletter import views

app_name = "newsletter"

urlpatterns = (
    path('create/', views.create_subscriber, name='create'),
)
