from django.contrib.auth.models import UserManager
from django.db import models

class EventProfile(models.Model):
    user = models.OneToOneField('SpkrbarUser')
    name = models.CharField(max_length=140)
    description = models.CharField(max_length=800)

    def get_absolute_url(self):
        return "/user/" + self.user.username

    class Meta:
        app_label = 'core'
