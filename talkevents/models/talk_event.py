from django.db import models
from core.models import UserProfile
from talks.models import Talk
from events.models import Event


class TalkEvent(models.Model):
    talk = models.ForeignKey(Talk)
    event = models.ForeignKey(Event)

    date = models.DateTimeField()
    attendees = models.ManyToManyField(UserProfile)

    class Meta:
        app_label = 'talkevents'
