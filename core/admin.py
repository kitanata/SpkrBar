from django.contrib import admin
from .models import Talk, Location, UserProfile

class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'city', 'state']

class TalkAdmin(admin.ModelAdmin):
    list_display = ['name', 'speaker_name', 'location', 'date']

admin.site.register(Talk, TalkAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(UserProfile, admin.ModelAdmin)
