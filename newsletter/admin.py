from django.contrib import admin

from newsletter import models

# Register message model in admin panel
admin.site.register(models.Messages)

# Register subscriber model in admin panel
admin.site.register(models.Subscribers)
