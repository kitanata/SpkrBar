from django.db import models
from datetime import datetime

class TalkComment(models.Model):
    talk = models.ForeignKey('Talk', related_name='comments')
    commenter = models.ForeignKey('core.SpkrbarUser', null=True)
    comment = models.CharField(max_length=140)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'talks'
