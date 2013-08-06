from django.db import models

class TalkEvent(models.Model):
    talk = models.ForeignKey('talks.Talk', related_name='engagements')
    event = models.ForeignKey('events.Event', related_name='engagements')

    date = models.DateTimeField()
    attendees = models.ManyToManyField('core.SpkrbarUser', related_name='attending', blank=True)

    from_speaker = models.BooleanField(default=True) #False if from_planner
    vetoed = models.BooleanField(default=False)

    def __str__(self):
        return ' '.join([str(self.talk), str(self.event)])

    class Meta:
        app_label = 'talkevents'
