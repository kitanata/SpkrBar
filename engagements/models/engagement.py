from django.db import models

from django.utils import formats

class Engagement(models.Model):
    talk = models.ForeignKey('talks.Talk', related_name='engagements')

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    event_name = models.CharField(max_length=300, default="")
    date = models.DateField()
    time = models.TimeField()
    location = models.ForeignKey('locations.Location')
    room = models.CharField(max_length=1000)

    def __str__(self):
        return ' '.join([str(self.event_name), str(self.date.year), ' - ', self.room])

    class Meta:
        app_label = 'engagements'
