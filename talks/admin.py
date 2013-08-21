from django.contrib import admin
from .models import *

class TalkAdmin(admin.ModelAdmin):
    list_display = ['name']

class TalkSlideDeckAdmin(admin.ModelAdmin):
    list_display = ['talk_name', 'source', 'data', 'aspect']

class TalkVideoAdmin(admin.ModelAdmin):
    list_display = ['talk_name', 'source', 'data', 'aspect']

class TalkCommentAdmin(admin.ModelAdmin):
    list_display = ['talk', 'comment']

admin.site.register(Talk, TalkAdmin)
admin.site.register(TalkComment, TalkCommentAdmin)
admin.site.register(TalkSlideDeck, TalkSlideDeckAdmin)
admin.site.register(TalkVideo, TalkVideoAdmin)

admin.site.register(TalkTag, admin.ModelAdmin)
admin.site.register(TalkPhoto, admin.ModelAdmin)
admin.site.register(TalkRating, admin.ModelAdmin)
