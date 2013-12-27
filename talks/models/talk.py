from django.db import models
from django.db.models import Q

class Talk(models.Model):
    speaker = models.ForeignKey('core.SpkrbarUser', related_name="talks")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=140)
    abstract = models.CharField(max_length=4000)

    published = models.BooleanField(default=True)

    tags = models.ManyToManyField(
        'talks.TalkTag', related_name='talks', blank=True)

    class Meta:
        app_label = 'talks'

    def __unicode__(self):
        return unicode(self.name)

    def get_absolute_url(self):
        return "/talk/" + str(self.pk)

    @classmethod
    def published_talks(klass, user_profile=None):
        if user_profile:
            return klass.objects.filter(
                    Q(speaker__published=True, published=True) | Q(speaker=user_profile))
        else:
            return klass.objects.filter(speaker__published=True, published=True)
