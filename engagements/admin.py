from django.contrib import admin
from models import Engagement

class EngagementAdmin(admin.ModelAdmin):
    search_fields = ['talk', 'event_name', 'room', 'date', 'time']
    list_display = ('talk', 'event_name', 'room', 'date', 'time')

admin.site.register(Engagement, EngagementAdmin)
