from django.db import models

class TalkEvent(models.Model):
    talk = models.ForeignKey('talks.Talk')
    event = models.ForeignKey('events.Event')

    date = models.DateTimeField()
    attendees = models.ManyToManyField('core.SpkrbarUser', related_name='attending')

    class Meta:
        app_label = 'talkevents'
