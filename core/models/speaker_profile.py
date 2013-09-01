from django.db import models

class SpeakerProfile(models.Model):
    user = models.OneToOneField('SpkrbarUser')
    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)

    about_me = models.CharField(max_length=4000, blank=True)

    photo = models.ImageField(upload_to="photo", blank=True)

    tags = models.ManyToManyField('core.ProfileTag', blank=True)

    def get_absolute_url(self):
        return "/profile/" + self.user.username

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

    def __unicode__(self):
        return self.user.get_full_name()

    class Meta:
        app_label = 'core'
