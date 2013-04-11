from django.contrib import admin
from .models import Talk, TalkTag, TalkReview

class TalkAdmin(admin.ModelAdmin):
    list_display = ['name', 'speaker_name', 'location', 'date']

admin.site.register(Talk, TalkAdmin)
admin.site.register(TalkTag, admin.ModelAdmin)
admin.site.register(TalkReview, admin.ModelAdmin)
