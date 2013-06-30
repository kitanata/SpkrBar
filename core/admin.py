from django.contrib import admin
from core.models import SpeakerProfile, EventProfile, SpeakerTag, SpeakerLink

admin.site.register(SpeakerProfile, admin.ModelAdmin)
admin.site.register(EventProfile, admin.ModelAdmin)
admin.site.register(SpeakerTag, admin.ModelAdmin)
admin.site.register(SpeakerLink, admin.ModelAdmin)
