from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from datetime import datetime


class Location(models.Model):
    name = models.CharField(max_length=140)
    address = models.CharField(max_length=140)
    city = models.CharField(max_length=140)
    state = models.CharField(max_length=140)
    zip_code = models.CharField(max_length=9)

    def __str__(self):
        return self.name


class UserTag(models.Model):
    name = models.CharField(max_length=140)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    photo = models.ImageField(upload_to="photo")
    about_me = models.CharField(max_length=500)
    location = models.ForeignKey(Location, null=True)
    following = models.ManyToManyField('self', related_name="followers", symmetrical=False)

    tags = models.ManyToManyField(UserTag)

    def __str__(self):
        return self.user.username



class UserLink(models.Model):
    FACEBOOK = 'FACEBOOK'
    TWITTER = 'TWITTER'
    LINKEDIN = 'LINKEDIN'
    GITHUB = 'GITHUB'
    BLOG = 'BLOG'
    WEBSITE = 'WEBSITE'

    LINK_TYPE_CHOICES = (
        (FACEBOOK, 'Facebook'),
        (TWITTER, 'Twitter'),
        (LINKEDIN, 'LinkedIn'),
        (GITHUB, 'GitHub'),
        (BLOG, 'Blog'),
        (WEBSITE, 'Other Website'),
    )

    type_name = models.CharField(max_length=40, choices=LINK_TYPE_CHOICES, default=TWITTER)
    url_target = models.URLField(max_length=140)

    profile = models.ForeignKey(UserProfile)

    def __str__(self):
        return self.link_name


def create_profile(sender, **kw):
    user = kw["instance"]
    if kw["created"]:
        profile = UserProfile()
        profile.user = user
        profile.save()

post_save.connect(create_profile, sender=User)
