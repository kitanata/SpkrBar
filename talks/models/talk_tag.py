from django.db import models

class TalkTag(models.Model):
    name = models.CharField(max_length=140)

    def __str__(self):
        return str(self.name)

    class Meta:
        app_label = 'talks'
