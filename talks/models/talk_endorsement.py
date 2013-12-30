from django.db import models

class TalkEndorsement(models.Model):
    user = models.ForeignKey('core.SpkrbarUser', related_name="endorsements")
    talk = models.ForeignKey('talks.Talk', related_name="endorsements")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'talks'

    def __unicode__(self):
        return unicode(self.speaker.get_full_name()) + unicode(self.talk.name)
