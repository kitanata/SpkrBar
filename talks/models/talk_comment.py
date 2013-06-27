from django.db import models
from datetime import datetime

class TalkComment(models.Model):
    talk = models.ForeignKey('Talk')
    reviewer = models.ForeignKey('core.UserProfile', null=True)
    comment = models.CharField(max_length=140)
    datetime = models.DateTimeField(default=datetime.now())

    class Meta:
        app_label = 'talks'
