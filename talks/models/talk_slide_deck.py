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
            return "<script async class='speakerdeck-embed' data-id='%s' data-ratio='%f' src='//speakerdeck.com/assets/embed.js'></script>" % (self.embed_data, self.aspect)
        return ""

    @classmethod
    def from_embed(cls, talk, text, source=None):
        deck = TalkSlideDeck()
        deck.talk = talk

        embed = text
        embed = embed.split(' ')
        embed = [x.split('=') for x in embed]
        embed = [x for x in embed if len(x) == 2]
        embed = {x[0]: x[1].strip(""" "'""") for x in embed}

        if not source:
            if 'slideshare' in text.lower():
                deck.source = SLIDESHARE
            else:
                deck.source = SPEAKERDECK
        else:
            deck.source = source

        if deck.source == SLIDESHARE:
            deck.embed_data = embed['src']
            w = embed['width']
            h = embed['height']
            deck.aspect = int(w) / float(h) if float(h) != 0 else 0
        elif deck.source == SPEAKERDECK:
            deck.embed_data = embed['data-id']
            deck.aspect = float(embed['data-ratio'])
        else:
            return None

        return deck
