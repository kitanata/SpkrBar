from django.db import models

class TalkLink(models.Model):
    talk = models.ForeignKey('Talk', related_name='links')
    name = models.CharField(max_length=140, blank=True)
    url = models.URLField()

    class Meta:
        app_label = 'talks'
