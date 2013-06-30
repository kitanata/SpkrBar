from django.db import models
from django.db.models import Q

class Event(models.Model):
    owner = models.ForeignKey('core.EventUser')

    location = models.ForeignKey('locations.Location')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    accept_submissions = models.BooleanField(default=False)
    attendees = models.ManyToManyField('core.NormalUser', related_name='events_attending', blank=True)

    class Meta:
        app_label = 'events'

    def get_absolute_url(self):
        return "/event/" + str(self.pk)
