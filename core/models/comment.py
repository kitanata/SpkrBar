from django.db import models
from datetime import datetime

class Comment(models.Model):
    user = models.ForeignKey('core.SpkrbarUser')
    parent = models.ForeignKey('self', related_name='children', null=True)
    comment = models.CharField(max_length=140)
    datetime = models.DateTimeField(default=datetime.now())

    class Meta:
        app_label = 'core'
