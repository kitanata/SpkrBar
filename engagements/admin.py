from django.contrib import admin
from models import Engagement

class EngagementAdmin(admin.ModelAdmin):
    search_fields = ['talk', 'event', 'date']
    list_display = ('talk', 'event', 'date')
    list_filter = ('event',)

admin.site.register(Engagement, EngagementAdmin)
