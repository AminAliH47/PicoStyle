from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.models import User

UserAdmin.fieldsets += ('Seller', {'fields': (
    'is_seller', 'company_name', 'co_address', 'co_country_registered', 'co_website_address', 'co_email',
    'about_manager_en', 'about_manager_ru', 'about_manager_it', 'phone_number', 'products_type', 'brand_name',
    'about_brand_en', 'about_brand_ru', 'about_brand_it', 'brand_logo', 'is_brand', 'branch_address',
)}), ('Author', {'fields': ('is_author',)}), ('Advance', {'fields': ('is_entrepreneur',)})
admin.site.register(User, UserAdmin)
