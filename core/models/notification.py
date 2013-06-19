from datetime import datetime

from django.db import models

class Notification(models.Model):
    profile = models.ForeignKey(UserProfile)
    message = models.CharField(max_length=300)
    date = models.DateTimeField(default=datetime.now())

    @classmethod
    def create(klass, profile, message):
        note = klass()
        note.profile = profile
        note.message = message
        note.save()

        return note
