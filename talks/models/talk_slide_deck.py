from django.db import models

from choices import *

class TalkSlideDeck(models.Model):
    talk = models.ForeignKey('Talk')
    source = models.CharField(max_length=40, choices=SLIDE_TYPE_CHOICES, default=SLIDESHARE)
    data = models.CharField(max_length=140)
    aspect = models.FloatField()

    class Meta:
        app_label = 'talks'

    def talk_name(self):
        return self.talk.name
