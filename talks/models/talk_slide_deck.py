from django.db import models

from choices import *

class TalkSlideDeck(models.Model):
    talk = models.ForeignKey('Talk', related_name='slides')
    source = models.CharField(max_length=40, choices=SLIDE_TYPE_CHOICES, default=SLIDESHARE)
    embed_data = models.CharField(max_length=140)
    aspect = models.FloatField()

    class Meta:
        app_label = 'talks'

    def talk_name(self):
        return self.talk.name

    def build_embed_code(self):
        if self.source == "SLIDESHARE":
            height = 300 * self.aspect
            return "<iframe src='%s' width='300' height='%d' frameborder='0' marginwidth='0'"
            " marginheight='0' scrolling='no' style='border:1px solid #CCC;border-width:1px 1px 0;margin-bottom:5px'"
            " allowfullscreen webkitallowfullscreen mozallowfullscreen></iframe>" % (self.embed_data, height)
        elif self.source == "SPEAKERDECK":
            return "<script class='speakerdeck-embed' async data-id='%s' data-ratio='%d' src='//speakerdeck.com/assets/embed.js'></script>" % (self.embed_data, self.aspect)
        return ""
