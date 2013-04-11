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


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    photo = models.ImageField(upload_to="photo")
    about_me = models.CharField(max_length=500)
    location = models.ForeignKey(Location, null=True)
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


def create_profile(sender, **kw):
    user = kw["instance"]
    if kw["created"]:
        profile = UserProfile()
        profile.user = user
        profile.save()

post_save.connect(create_profile, sender=User)
