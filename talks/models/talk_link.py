from django.db import models

class TalkLink(models.Model):
    talk = models.ForeignKey(Talk)
    name = models.CharField(max_length=140)
    url = models.URLField()
