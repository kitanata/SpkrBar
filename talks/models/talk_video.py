from django.db import models

from choices import *

class TalkVideo(models.Model):
    talk = models.ForeignKey('Talk', related_name='videos')
    source = models.CharField(max_length=40, choices=VIDEO_TYPE_CHOICES, default=YOUTUBE)
    embed_data = models.CharField(max_length=140)
    aspect = models.FloatField()

    class Meta:
        app_label = 'talks'

    def talk_name(self):
        return self.talk.name

    def build_embed_code(self):
        return "<iframe width='100%%' height='400px' src='%s' frameborder='0' webkitAllowFullScreen, mozallowfullscreen, allowfullscreen></iframe>" % (self.embed_data,)
