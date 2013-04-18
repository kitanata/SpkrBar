from django.contrib import admin
from .models import Talk, TalkTag, TalkReview, TalkVideo

class TalkAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'location', 'date']

class TalkVideoAdmin(admin.ModelAdmin):
    list_display = ['talk_name', 'video_type', 'url_target']

admin.site.register(Talk, TalkAdmin)
admin.site.register(TalkTag, admin.ModelAdmin)
admin.site.register(TalkReview, admin.ModelAdmin)
admin.site.register(TalkVideo, TalkVideoAdmin)
