from django.contrib import admin
from core.models import *

class UserLinkAdmin(admin.ModelAdmin):
    list_display = ['user', 'type_name', 'url_target']

admin.site.register(SpkrbarUser, admin.ModelAdmin)
admin.site.register(UserTag, admin.ModelAdmin)
admin.site.register(UserLink, UserLinkAdmin)
admin.site.register(Notification, admin.ModelAdmin)
