from django.db import models

class UserFollowing(models.Model):
    user = models.ForeignKey('core.SpkrbarUser', related_name="following")
    following = models.ForeignKey('core.SpkrbarUser', related_name="followers")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'core'

    def __unicode__(self):
        return unicode(self.following.get_full_name())
