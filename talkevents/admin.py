from django.contrib import admin
from models import TalkEvent, TalkEventSubmission

admin.site.register(TalkEvent, admin.ModelAdmin)
admin.site.register(TalkEventSubmission, admin.ModelAdmin)
