from django.contrib.auth.models import UserManager
from django.db import models

from core.models import SpkrbarBaseUser

class NormalUser(SpkrbarBaseUser):
    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)

    about_me = models.CharField(max_length=500)

    photo = models.ImageField(upload_to="photo")

    following = models.ManyToManyField('self', related_name="followers", symmetrical=False)
    tags = models.ManyToManyField('UserTag')

    objects = UserManager()

    def get_full_name(self):
        return ' '.join([str(self.first_name), str(self.last_name)])

    def get_short_name(self):
        return str(self.first_name)

    def get_absolute_url(self):
        return "/user/" + self.username

    def published_upcoming_events_attending(self, user_profile=None):
        if user_profile:
            events = self.events_attending.filter(
                    Q(talk__published=True) | Q(talk__speaker=request.user))
        else:
            events = self.events_attending.filter(talk__published=True)
        
        return events.filter(date__gt=datetime.now()).order_by('date')

    def published_past_events_attended(self, user_profile=None):
        if user_profile:
            events = self.events_attending.filter(
                    Q(talk__published=True) | Q(talk__speaker=request.user))
        else:
            events = self.events_attending.filter(talk__speaker__published=True)

        return events.filter(date__lt=datetime.now()).order_by('-date')

    class Meta:
        app_label = 'core'
