from random import randint

from django.contrib import admin

from extensions.extensions import inactivate_status
from products import models
from products.models import ProductsCategory


class ProductImagesInlines(admin.StackedInline):
    model = models.ProductImages


# Register products in admin panel
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status',)
    inlines = (ProductImagesInlines,)
    exclude = ('slug',)

    # Save product in all parent category
    def save_related(self, request, form, formsets, change):
        super(ProductsAdmin, self).save_related(request, form, formsets, change)
        form.instance.type = [x.title for x in form.instance.all_categories][1]

        if not form.instance.code2:
            code = f"{form.instance.seller.id}{[x.title for x in form.instance.all_categories][-1][0]}{form.instance.type[0]}{randint(1000, 9999)}"
            form.instance.code2 = code

        form.save()
        form.save_m2m()
        for x in form.instance.all_categories:
            category = models.ProductsCategory.objects.get(id=x.id)
            if category not in form.instance.category.all():
                form.instance.category.add(category)


admin.site.register(models.Products, ProductsAdmin)


# Register products category in admin panel
class ProductsCategoryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'parent', 'slug', 'active',)

    # exclude = ('slug',)

    def save_form(self, request, form, change):
        category = form.instance
        categories = category.children.all()
        if categories:
            if not category.active:
                for cat in categories:
                    cat.active = False
                    if cat.children.all():
                        inactivate_status(cat, category)
                ProductsCategory.objects.bulk_update(categories, fields=['active'])

        parents = category.all_parent
        if category.parent:
            if category.active:
                for cat in parents:
                    cat.active = True
                ProductsCategory.objects.bulk_update(parents, fields=['active'])
        return super(ProductsCategoryAdmin, self).save_form(request, form, change)


admin.site.register(models.ProductsCategory, ProductsCategoryAdmin)

# Register products tag in admin panel
admin.site.register(models.ProductsTag)

# Register product images in admin panel
admin.site.register(models.ProductImages)

# Register products type in admin panel
admin.site.register(models.ProductsType)

# Register products material in admin panel
admin.site.register(models.ProductMaterial)

# Register shoe sole in admin panel
admin.site.register(models.ShoeSole)


# Register product price percent in admin panel
class ProductPercentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'slug',)


admin.site.register(models.ProductPercent, ProductPercentAdmin)

# Register product size in admin panel
admin.site.register(models.ProductSize)


# Register show/hide status in admin panel
class ShowProductsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'show_retail_price', 'show_wholesale_price',)


admin.site.register(models.ShowProducts, ShowProductsAdmin)
