from django.urls import path
from main import views

app_name = 'main'

urlpatterns = (
    path('', views.Index.as_view(), name='index'),
    path('change-lang', views.change_lang, name='change_lang'),
    # retailer
    path('become-retailer', views.BecomeRetailer.as_view(), name='become_retailer'),
    path('thanks', views.thanks, name='thanks'),
    # store and agent
    path('store-and-agent', views.store_agent, name='store_agent'),
    # Size guide
    path('size-guide/', views.MainSizeGuide.as_view(), name='size_guide'),
    path('size-guide/women/', views.SizeGuideWomen.as_view(), name='sg_women'),
    path('size-guide/men/', views.SizeGuideMen.as_view(), name='sg_men'),
    # Work with us
    path('work-with-us/', views.WorkWithUsList.as_view(), name='work_with_us'),
    # Special projects
    path('special-projects/', views.SpecialProjectsList.as_view(), name='special_projects'),
)
