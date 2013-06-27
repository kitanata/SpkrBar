from django.contrib import admin
from core.models import NormalUser, EventUser, UserTag, UserLink

admin.site.register(NormalUser, admin.ModelAdmin)
admin.site.register(EventUser, admin.ModelAdmin)
admin.site.register(UserTag, admin.ModelAdmin)
admin.site.register(UserLink, admin.ModelAdmin)
