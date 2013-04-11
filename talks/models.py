from django.db import models
from datetime import datetime

from core.models import UserProfile, Location

class TalkTag(models.Model):
    name = models.CharField(max_length=140)



class Talk(models.Model):
    speakers = models.ManyToManyField(UserProfile)
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=800)
    location = models.ForeignKey(Location)
    date = models.DateTimeField(default=datetime.now())

    tags = models.ManyToManyField(TalkTag)

    def speaker_name(self):
        return self.speaker.get_full_name()

    def __str__(self):
        return self.name



class TalkReview(models.Model):
    talk = models.ForeignKey(Talk)
    reviewer = models.ForeignKey(UserProfile)
    rating = models.IntegerField(default=3)
    comments = models.CharField(max_length=140)
