from datetime import datetime

from django.db import models

class Notification(models.Model):
    user = models.ForeignKey('core.SpkrbarUser', related_name='notifications')
    title = models.CharField(max_length=140, default="Notification")
    message = models.CharField(max_length=1000)
    dismissed = models.BooleanField(default=False)
    date = models.DateTimeField(default=datetime.now())

    class Meta:
        app_label = 'core'

    @classmethod
    def create(klass, profile, message):
        note = klass()
        note.profile = profile
        note.message = message
        note.save()

        return note

    def __str__(self):
        return self.message
