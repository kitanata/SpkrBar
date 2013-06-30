from django.contrib import admin
from .models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ['owner', 'start_date', 'end_date', 'location', 'accept_submissions']

admin.site.register(Event, EventAdmin)
