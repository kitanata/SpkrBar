from datetime import datetime

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from locations.models import Location
from talks.models import Talk
from events.models import Event

class UserTag(models.Model):
    name = models.CharField(max_length=140)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    photo = models.ImageField(upload_to="photo")
    about_me = models.CharField(max_length=500)
    published = models.BooleanField(default=True)

    following = models.ManyToManyField('self', related_name="followers", symmetrical=False)

    tags = models.ManyToManyField(UserTag)

    def __str__(self):
        return self.user.username


    def get_absolute_url(self):
        return "/speaker/" + self.user.username


    def get_published_events(self):
        return self.event_set.filter(published=True, owner__published=True).all()


    def published_upcoming_events_attending(self, user_profile=None):
        if user_profile:
            events = self.events_attending.filter(
                    Q(talk__published=True, talk__speaker__published=True
                        ) | Q(talk__speaker=request.user.get_profile()))
        else:
            events = self.events_attending.filter(talk__published=True, talk__speaker__published=True)
        
        return events.filter(date__gt=datetime.now()).order_by('date')

    def published_past_events_attended(self, user_profile=None):
        if user_profile:
            events = self.events_attending.filter(
                    Q(talk__published=True, talk__speaker__published=True
                        ) | Q(talk__speaker=request.user.get_profile()))
        else:
            events = self.events_attending.filter(talk__published=True, talk__speaker__published=True)

        return events.filter(date__lt=datetime.now()).order_by('-date')



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


class Notification(models.Model):
    profile = models.ForeignKey(UserProfile)
    message = models.CharField(max_length=300)
    date = models.DateTimeField(default=datetime.now())

    @classmethod
    def create(klass, profile, message):
        note = klass()
        note.profile = profile
        note.message = message
        note.save()

        return note


class TalkEvent(models.Model):
    talk = models.ForeignKey(Talk)
    event = models.ForeignKey(Event)

    date = models.DateTimeField()
    attendees = models.ManyToManyField(UserProfile)


class TalkEventSubmission(models.Model):
    talk = models.ForeignKey(Talk)
    event = models.ForeignKey(Event)
    date = models.DateTimeField(default=datetime.now())

    event_accepts = models.BooleanField(default=False)
    speaker_accepts = models.BooleanField(default=False)


def create_profile(sender, **kw):
    user = kw["instance"]
    if kw["created"]:
        profile = UserProfile()
        profile.user = user
        profile.save()

post_save.connect(create_profile, sender=User)
