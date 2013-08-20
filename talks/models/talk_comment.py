from django.db import models
from datetime import datetime

class TalkComment(models.Model):
    talk = models.ForeignKey('Talk')
    comment = models.ForeignKey('core.Comment')

    class Meta:
        app_label = 'talks'
