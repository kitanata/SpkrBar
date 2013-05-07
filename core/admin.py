from django.contrib import admin
from .models import UserProfile, UserTag, UserLink

admin.site.register(UserProfile, admin.ModelAdmin)
admin.site.register(UserTag, admin.ModelAdmin)
admin.site.register(UserLink, admin.ModelAdmin)
