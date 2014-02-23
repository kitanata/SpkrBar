from django.contrib import admin
from core.models import *

class UserLinkAdmin(admin.ModelAdmin):
    list_display = ['user', 'type_name', 'url_target']

class SpkrbarUserAdmin(admin.ModelAdmin):
    list_filter = ['plan_name', 'is_event_manager', 'billed_forever']
    search_fields = ['full_name', 'email']

admin.site.register(SpkrbarUser, SpkrbarUserAdmin)
admin.site.register(UserTag, admin.ModelAdmin)
admin.site.register(UserLink, UserLinkAdmin)
admin.site.register(Notification, admin.ModelAdmin)
