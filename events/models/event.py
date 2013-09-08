from django.db import models
from django.db.models import Q

class Event(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    name = models.CharField(max_length=300, default="")
    year = models.PositiveSmallIntegerField(choices=[(i,i) for i in range(1985,2031)])
    location = models.ForeignKey('locations.Location')

    def __unicode__(self):
        return u' '.join([unicode(self.name), u' - ', unicode(self.year)])

    def get_absolute_url(self):
        return "/event/" + str(self.pk)

    class Meta:
        app_label = 'events'
