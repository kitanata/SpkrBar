from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    is_speaker = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Location(models.Model):
    name = models.CharField(max_length=140)
    address = models.CharField(max_length=140)
    city = models.CharField(max_length=140)
    state = models.CharField(max_length=140)

    def __str__(self):
        return self.name

class Talk(models.Model):
    speaker = models.ForeignKey(User)
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=800)
    location = models.ForeignKey(Location)
    date = models.DateTimeField(default=datetime.now())

    def speaker_name(self):
        return self.speaker.get_full_name()

    def __str__(self):
        return self.name
