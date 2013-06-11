from django.contrib import admin
from .models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'published', 'start_date', 'end_date', 'location']

admin.site.register(Event, EventAdmin)
