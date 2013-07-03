from django.db import models

class ProfileTag(models.Model):
    name = models.CharField(max_length=140)

    class Meta:
        app_label = 'core'

    def __str__(self):
        return self.name