from django.contrib import admin
from models import TalkEvent, TalkEventSubmission

class TalkEventAdmin(admin.ModelAdmin):
    search_fields = ['talk', 'event', 'date']
    list_display = ('talk', 'event', 'date')
    list_filter = ('event',)

admin.site.register(TalkEvent, TalkEventAdmin)
admin.site.register(TalkEventSubmission, admin.ModelAdmin)
