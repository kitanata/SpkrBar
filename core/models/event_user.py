from django.contrib.auth.models import UserManager
from core.models import SpkrbarBaseUser
from django.db import models

class EventUser(SpkrbarBaseUser):
    name = models.CharField(max_length=140)
    description = models.CharField(max_length=800)

    objects = UserManager()

    def get_full_name(self):
        return str(self.name)

    def get_short_name(self):
        return str(self.name)

    def get_absolute_url(self):
        return "/event/" + self.username

    class Meta:
        app_label = 'core'
