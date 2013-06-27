from django.db import models

from choices import *

class TalkVideo(models.Model):
    talk = models.ForeignKey('Talk')
    source = models.CharField(max_length=40, choices=VIDEO_TYPE_CHOICES, default=YOUTUBE)
    data = models.CharField(max_length=140)
    aspect = models.FloatField()

    class Meta:
        app_label = 'talks'

    def talk_name(self):
        return self.talk.name
