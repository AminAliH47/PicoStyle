from django.contrib import admin

# Model import
from news.models import News, NewsTag, CategoryNews


# Register News
class NewsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status',)
    exclude = ('slug',)
    autocomplete_fields = ('category',)


admin.site.register(News, NewsAdmin)


# Register CategoryNews
class CategoryNewsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'active',)
    exclude = ('slug',)
    search_fields = ('category__news',)


admin.site.register(CategoryNews, CategoryNewsAdmin)

# Register NewsTag
admin.site.register(NewsTag)
