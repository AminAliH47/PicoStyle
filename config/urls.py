from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import (
    path,
    include,
)
from config import settings
from pages.views import PagesDetail

admin.site.site_header = "PicoStyle management"

# Handle custom error pages
handler404 = 'main.views.page_not_found'
handler500 = 'main.views.server_error'

urlpatterns = []

urlpatterns += i18n_patterns(
    path('account/', include('account.urls')),
    path('news/', include('news.urls')),
    path('brands/', include('brands.urls')),
    path('entrepreneurs/', include('entrepreneur.urls')),
    path('products/', include('products.urls')),
    path('favorites/', include('favorite.urls')),
    path('newsletter/', include('newsletter.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('main.urls')),
    path('pico-style/', admin.site.urls),
    # Pages sections
    path('<str:slug>', PagesDetail.as_view(), name="pages"),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
