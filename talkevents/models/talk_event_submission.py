from datetime import datetime

from django.db import models
from talks.models import Talk
from events.models import Event

class TalkEventSubmission(models.Model):
    talk = models.ForeignKey(Talk)
    event = models.ForeignKey(Event)
    date = models.DateTimeField(default=datetime.now())

    event_accepts = models.BooleanField(default=False)
    speaker_accepts = models.BooleanField(default=False)

    class Meta:
        app_label = 'talkevents'
