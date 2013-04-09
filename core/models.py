from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from datetime import datetime


class Location(models.Model):
    name = models.CharField(max_length=140)
    address = models.CharField(max_length=140)
    city = models.CharField(max_length=140)
    state = models.CharField(max_length=140)

    def __str__(self):
        return self.name



class UserTag(models.Model):
    name = models.CharField(max_length=140)



class TalkTag(models.Model):
    name = models.CharField(max_length=140)



class UserProfile(models.Model):
    user = models.OneToOneField(User)
    location = models.ForeignKey(Location, null=True)
    about_me = models.CharField(max_length=500)
    following = models.ManyToManyField('self', related_name='following')
    followers = models.ManyToManyField('self', related_name='followers')

    tags = models.ManyToManyField(UserTag)

    def __str__(self):
        return self.user.username



class UserLink(models.Model):
    type_name = models.CharField(max_length=40)
    link_name = models.CharField(max_length=200)
    url_target = models.URLField(max_length=140)

    profile = models.ForeignKey(UserProfile)



class Talk(models.Model):
    speakers = models.ManyToManyField(UserProfile)
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=800)
    location = models.ForeignKey(Location)
    date = models.DateTimeField(default=datetime.now())

    tags = models.ManyToManyField(TalkTag)

    def speaker_name(self):
        return self.speaker.get_full_name()

    def __str__(self):
        return self.name



class TalkReview(models.Model):
    talk = models.ForeignKey(Talk)
    reviewer = models.ForeignKey(UserProfile)
    rating = models.IntegerField(default=3)
    comments = models.CharField(max_length=140)


def create_profile(sender, **kw):
    user = kw["instance"]
    if kw["created"]:
        profile = UserProfile()
        profile.user = user
        profile.save()

post_save.connect(create_profile, sender=User)
