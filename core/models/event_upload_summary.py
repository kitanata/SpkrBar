from django.db import models
from core.models import EventUpload

class EventUploadSummary(models.Model):
    event_upload = models.ForeignKey(EventUpload, related_name='summary')
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=600)

    class Meta:
        app_label = 'core'
        #states are 

    @classmethod
    def create(cls, event_upload, name, description):
        summary = EventUploadSummary()
        summary.event_upload = event_upload
        summary.name = name
        summary.description = description
        return summary