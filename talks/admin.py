from django.contrib import admin
from .models import *

class TalkAdmin(admin.ModelAdmin):
    list_display = ['name', 'abstract']

class TalkSlideDeckAdmin(admin.ModelAdmin):
    list_display = ['talk_name', 'source', 'embed_data', 'aspect']

class TalkVideoAdmin(admin.ModelAdmin):
    list_display = ['talk_name', 'source', 'embed_data', 'aspect']

class TalkCommentAdmin(admin.ModelAdmin):
    list_display = ['talk', 'user', 'comment', 'updated_at', 'created_at']

admin.site.register(Talk, TalkAdmin)
admin.site.register(TalkComment, TalkCommentAdmin)
admin.site.register(TalkSlideDeck, TalkSlideDeckAdmin)
admin.site.register(TalkVideo, TalkVideoAdmin)

admin.site.register(TalkTag, admin.ModelAdmin)
