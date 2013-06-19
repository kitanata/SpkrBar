from django.db import models

class TalkVideo(models.Model):
    talk = models.ForeignKey(Talk)
    source = models.CharField(max_length=40, choices=VIDEO_TYPE_CHOICES, default=YOUTUBE)
    data = models.CharField(max_length=140)
    aspect = models.FloatField()

    def talk_name(self):
        return self.talk.name
