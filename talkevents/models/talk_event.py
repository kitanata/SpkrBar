from django.db import models

from django.utils import formats

class TalkEvent(models.Model):
    talk = models.ForeignKey('talks.Talk', related_name='engagements')
    event = models.ForeignKey('events.Event', related_name='engagements')

    date = models.DateTimeField()
    attendees = models.ManyToManyField('core.SpkrbarUser', related_name='attending', blank=True)

    from_speaker = models.BooleanField(default=True) #False if from_planner
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return ' '.join([str(self.talk), str(self.event)])

    def formatted_date(self):
        return formats.date_format(self.date, "SHORT_DATETIME_FORMAT").split(' ')[0]

    def formatted_time(self):
        return ' '.join(formats.date_format(self.date, "SHORT_DATETIME_FORMAT").split(' ')[1:])

    class Meta:
        app_label = 'talkevents'
