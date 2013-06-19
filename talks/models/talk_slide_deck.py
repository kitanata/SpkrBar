from django.db import models

class TalkSlideDeck(models.Model):
    talk = models.ForeignKey(Talk)
    source = models.CharField(max_length=40, choices=SLIDE_TYPE_CHOICES, default=SLIDESHARE)
    data = models.CharField(max_length=140)
    aspect = models.FloatField()

    def talk_name(self):
        return self.talk.name
