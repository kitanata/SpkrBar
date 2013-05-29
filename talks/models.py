from django.db import models
from django.db.models import Q
from datetime import datetime

class TalkTag(models.Model):
    name = models.CharField(max_length=140)


class Talk(models.Model):
    speaker = models.ForeignKey('core.UserProfile')

    name = models.CharField(max_length=140)
    abstract = models.CharField(max_length=800)

    published = models.BooleanField(default=True)

    tags = models.ManyToManyField(TalkTag)

    endorsements = models.ManyToManyField('core.UserProfile', related_name='talks_endorsed')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/talk/" + str(self.pk)

    @classmethod
    def published_talks(klass, user_profile=None):
        if user_profile:
            return klass.objects.filter(
                    Q(speaker__published=True, published=True) | Q(speaker=user_profile))
        else:
            return klass.objects.filter(speaker__published=True, published=True)


class TalkComment(models.Model):
    talk = models.ForeignKey(Talk)
    reviewer = models.ForeignKey('core.UserProfile', null=True)
    comment = models.CharField(max_length=140)
    datetime = models.DateTimeField(default=datetime.now())


class TalkVideo(models.Model):
    YOUTUBE = 'YOUTUBE'
    VIMEO = 'VIMEO'

    LINK_TYPE_CHOICES = (
        (YOUTUBE, 'Youtube'),
        (VIMEO, 'Vimeo'),
    )

    talk = models.ForeignKey(Talk)
    video_type = models.CharField(max_length=40, choices=LINK_TYPE_CHOICES, default=YOUTUBE)
    url_target = models.URLField(max_length=140)

    def talk_name(self):
        return self.talk.name
