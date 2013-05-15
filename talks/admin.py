from django.contrib import admin
from .models import Talk, TalkTag, TalkComment, TalkVideo

class TalkAdmin(admin.ModelAdmin):
    list_display = ['name']

class TalkVideoAdmin(admin.ModelAdmin):
    list_display = ['talk_name', 'video_type', 'url_target']

class TalkCommentAdmin(admin.ModelAdmin):
    list_display = ['talk', 'reviewer', 'comment', 'datetime']

admin.site.register(Talk, TalkAdmin)
admin.site.register(TalkTag, admin.ModelAdmin)
admin.site.register(TalkComment, TalkCommentAdmin)
admin.site.register(TalkVideo, TalkVideoAdmin)
