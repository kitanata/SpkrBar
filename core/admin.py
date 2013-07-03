from django.contrib import admin
from core.models import SpeakerProfile, EventProfile, ProfileTag, SpeakerLink

admin.site.register(SpeakerProfile, admin.ModelAdmin)
admin.site.register(EventProfile, admin.ModelAdmin)
admin.site.register(ProfileTag, admin.ModelAdmin)
admin.site.register(SpeakerLink, admin.ModelAdmin)
