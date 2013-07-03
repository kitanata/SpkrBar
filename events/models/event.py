from django.db import models
from django.db.models import Q

class Event(models.Model):
    owner = models.ForeignKey('core.EventProfile')

    location = models.ForeignKey('locations.Location')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    accept_submissions = models.BooleanField(default=False)
    attendees = models.ManyToManyField(
            'core.SpeakerProfile', related_name='events_attending', blank=True)


    def __str__(self):
        return ' '.join([str(self.owner.name), str(self.start_date.year)])


    def get_absolute_url(self):
        return "/event/" + str(self.pk)


    class Meta:
        app_label = 'events'
