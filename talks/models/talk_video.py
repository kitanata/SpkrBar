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

    @classmethod
    def from_embed(cls, talk, text):
        video = TalkVideo()
        video.talk = talk

        embed = text
        embed = embed.split(' ')
        embed = [x.split('=') for x in embed]
        embed = [x for x in embed if len(x) == 2]
        embed = {x[0]: x[1].strip(""" "'""") for x in embed}

        video.source = form.cleaned_data['source']

        if video.source == YOUTUBE or video.source == VIMEO:
            video.embed_data = embed['src']
            w = embed['width']
            h = embed['height']
            video.aspect = int(h) / float(w) if float(w) != 0 else 0
        else:
            return None

        return video
