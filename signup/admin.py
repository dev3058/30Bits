from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display=(
        'id','username','email_verified',
    )

admin.site.register(UserProfile,UserProfileAdmin)

# Register your models here.
