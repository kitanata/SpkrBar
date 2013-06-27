from datetime import datetime

from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    photo = models.ImageField(upload_to="photo")
    about_me = models.CharField(max_length=500)
    published = models.BooleanField(default=True)

    following = models.ManyToManyField('self', related_name="followers", symmetrical=False)

    tags = models.ManyToManyField('UserTag')

    class Meta:
        app_label = 'core'

    def __str__(self):
        return self.user.username


    def get_absolute_url(self):
        return "/speaker/" + self.user.username


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


def create_profile(sender, **kw):
    user = kw["instance"]
    if kw["created"]:
        profile = UserProfile()
        profile.user = user
        profile.save()

post_save.connect(create_profile, sender=User)
