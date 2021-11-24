from django.contrib import admin
from django.db import models
from .models import UrlLead, ImageStorage

class UrlLeadAdmin(admin.ModelAdmin):
    list_display = (
        'user','shortened_url','is_active','last_modified','is_public',
    )
admin.site.register(UrlLead,UrlLeadAdmin)

class ImageStorageAdmin(admin.ModelAdmin):
    list_display = (
        'user','image',
    )
admin.site.register(ImageStorage,ImageStorageAdmin)
