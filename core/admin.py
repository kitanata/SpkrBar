from django.contrib import admin
from core.models import *

class SpeakerLinkAdmin(admin.ModelAdmin):
    list_display = ['speaker', 'type_name', 'url_target']

admin.site.register(SpkrbarUser, admin.ModelAdmin)
admin.site.register(SpeakerProfile, admin.ModelAdmin)
admin.site.register(EventProfile, admin.ModelAdmin)
admin.site.register(ProfileTag, admin.ModelAdmin)
admin.site.register(SpeakerLink, SpeakerLinkAdmin)
