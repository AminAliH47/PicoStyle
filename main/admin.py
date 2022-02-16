from django.contrib import admin

# Models import
from main import models


# Register Site Setting
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('site_title', 'logo',)


admin.site.register(models.SiteSetting, SiteSettingAdmin)


# Register Main slideshow
class MainSliderAdmin(admin.ModelAdmin):
    list_display = ('__str__',)


admin.site.register(models.MainSlider, MainSliderAdmin)


# Register Brands slideshow
class BrandSliderAdmin(admin.ModelAdmin):
    list_display = ('__str__',)


admin.site.register(models.BrandsSlider, BrandSliderAdmin)


# Register Main Navbar
class MainNavbarAdmin(admin.ModelAdmin):
    list_display = ('__str__',)


admin.site.register(models.MainNavbar, MainNavbarAdmin)


# Register Main Navbar
class SubNavbarAdmin(admin.ModelAdmin):
    list_display = ('__str__',)


admin.site.register(models.SubNavbar, SubNavbarAdmin)

# Register social media
admin.site.register(models.SocialMedia)


# Register Main category
class MainCategoriesAdmin(admin.ModelAdmin):
    list_display = ('__str__',)


admin.site.register(models.MainCategories, MainCategoriesAdmin)

# Register Retailers
admin.site.register(models.Retailers)


# Register Store and agent
class StoreAgentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'country', 'country_code', 'active',)


admin.site.register(models.StoreAgent, StoreAgentAdmin)

# Register special projects
admin.site.register(models.SpecialProjects)

# Register work with us
admin.site.register(models.WorkWithUs)

# Register size guide
admin.site.register(models.SizeGuide)
