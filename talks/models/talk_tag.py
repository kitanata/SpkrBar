from django.db import models

class TalkTag(models.Model):
    name = models.CharField(max_length=140)
