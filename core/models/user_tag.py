from django.db import models

class UserTag(models.Model):
    name = models.CharField(max_length=140)

    class Meta:
        app_label = 'core'

    def __unicode__(self):
        return self.name
