from django.db import models
from django.db.models import Q

class Event(models.Model):
    owner = models.ForeignKey('core.UserProfile')
    name = models.CharField(max_length=140)
    description = models.CharField(max_length=800)
    accept_submissions = models.BooleanField(default=False)

    location = models.ForeignKey('locations.Location')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    attendees = models.ManyToManyField('core.UserProfile', related_name='events_attending', blank=True)

    class Meta:
        app_label = 'events'

    def get_absolute_url(self):
        return "/event/" + str(self.pk)

    @classmethod
    def published_events(klass, user_profile=None):
        if user_profile:
            return klass.objects.filter(
                    Q(owner__published=True, published=True) | Q(owner=user_profile))
        else:
            return klass.objects.filter(owner__published=True, published=True)
