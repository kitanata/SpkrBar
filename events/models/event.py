from django.db import models
from django.db.models import Q

class Event(models.Model):
    owner = models.ForeignKey('core.EventProfile', related_name="events")

    name = models.CharField(max_length=300, default="")
    location = models.ForeignKey('locations.Location')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    accept_submissions = models.BooleanField(default=False)
    attendees = models.ManyToManyField(
            'core.SpkrbarUser', related_name='events_attending', blank=True)
    endorsements = models.ManyToManyField(
            'core.SpkrbarUser', related_name='events_endorsed', blank=True)


    def __unicode__(self):
        if self.name:
            return u' '.join([unicode(self.owner.name), unicode(self.start_date.year), u' - ', unicode(self.name)])
        else:
            return u' '.join([unicode(self.owner.name), unicode(self.start_date.year)])


    def get_absolute_url(self):
        return "/event/" + str(self.pk)


    class Meta:
        app_label = 'events'
