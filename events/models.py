from datetime import datetime

from django.db import models
from django.db.models import Q

from talks.models import Talk
from locations.models import Location
from core.models import UserProfile

class Event(models.Model):
    talk = models.ForeignKey(Talk)
    location = models.ForeignKey(Location)
    date = models.DateTimeField(default=datetime.now())

    attendees = models.ManyToManyField(UserProfile, related_name='events_attending')

    @classmethod
    def published_events(klass, user_profile=None):
        if user_profile:
            return klass.objects.filter(
                    Q(talk__speaker__published=True, talk__published=True) | Q(talk__speaker=user_profile))
        else:
            return klass.objects.filter(talk__speaker__published=True, talk__published=True)

