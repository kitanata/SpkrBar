from django.contrib import admin
from .models import Location, UserProfile

class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'city', 'state']

admin.site.register(Location, LocationAdmin)
admin.site.register(UserProfile, admin.ModelAdmin)
