from django.db import models
from datetime import datetime

from core.models import UserProfile, Location

class TalkTag(models.Model):
    name = models.CharField(max_length=140)



class Talk(models.Model):
    speakers = models.ManyToManyField(UserProfile)
    name = models.CharField(max_length=140)
    abstract = models.CharField(max_length=800)
    published = models.BooleanField(default=True)

    photo = models.ImageField(upload_to="photo", blank=True)
    tags = models.ManyToManyField(TalkTag)

    endorsements = models.ManyToManyField(UserProfile, related_name='talks_endorsed')

    def __str__(self):
        return self.name


class TalkEvent(models.Model):
    talk = models.ForeignKey(Talk)
    location = models.ForeignKey(Location)
    date = models.DateTimeField(default=datetime.now())

    attendees = models.ManyToManyField(UserProfile, related_name='events_attending')


class TalkComment(models.Model):
    talk = models.ForeignKey(Talk)
    reviewer = models.ForeignKey(UserProfile, null=True)
    comment = models.CharField(max_length=140)
    datetime = models.DateTimeField(default=datetime.now())


class TalkVideo(models.Model):
    YOUTUBE = 'YOUTUBE'
    VIMEO = 'VIMEO'

    LINK_TYPE_CHOICES = (
        (YOUTUBE, 'Youtube'),
        (VIMEO, 'Vimeo'),
    )

    talk = models.ForeignKey(Talk)
    video_type = models.CharField(max_length=40, choices=LINK_TYPE_CHOICES, default=YOUTUBE)
    url_target = models.URLField(max_length=140)

    def talk_name(self):
        return self.talk.name
