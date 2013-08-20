from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.db import models

class SpkrbarUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_ATTENDEE = 'ATTENDEE'
    USER_TYPE_SPEAKER = 'SPEAKER'
    USER_TYPE_EVENT = 'EVENT'
    USER_TYPES = (
            (USER_TYPE_ATTENDEE, 'Attendee'),
            (USER_TYPE_SPEAKER, 'Speaker'),
            (USER_TYPE_EVENT, 'Event'),
        )

    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField()

    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    user_type = models.CharField(
            max_length=10, choices=USER_TYPES, default=USER_TYPE_SPEAKER)

    following = models.ManyToManyField('self', 
            related_name="followers", symmetrical=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'user_type']

    objects = UserManager()


    def __str__(self):
        return self.username


    def is_speaker(self):
        return self.user_type == SpkrbarUser.USER_TYPE_SPEAKER

    def is_event_planner(self):
        return self.user_type == SpkrbarUser.USER_TYPE_EVENT

    def is_attendee(self):
        return self.user_type == SpkrbarUser.USER_TYPE_ATTENDEE

    def get_full_name(self):
        profile = self.get_profile()

        if self.user_type == SpkrbarUser.USER_TYPE_SPEAKER:
            return u' '.join([unicode(profile.first_name), unicode(profile.last_name)])
        elif self.user_type == SpkrbarUser.USER_TYPE_ATTENDEE:
            return u' '.join([unicode(profile.first_name), unicode(profile.last_name)])
        elif self.user_type == SpkrbarUser.USER_TYPE_EVENT:
            return unicode(profile.name)
        else:
            return u'Error: Not a user'


    def get_short_name(self):
        profile = self.get_profile()

        if self.user_type == SpkrbarUser.USER_TYPE_SPEAKER:
            return str(profile.first_name)
        elif self.user_type == SpkrbarUser.USER_TYPE_ATTENDEE:
            return str(profile.first_name)
        elif self.user_type == SpkrbarUser.USER_TYPE_EVENT:
            return str(profile.name)
        else:
            return 'NOT_A_USER'


    def get_profile(self):
        if self.user_type == SpkrbarUser.USER_TYPE_SPEAKER:
            return self.speakerprofile
        elif self.user_type == SpkrbarUser.USER_TYPE_ATTENDEE:
            return self.attendeeprofile
        elif self.user_type == SpkrbarUser.USER_TYPE_EVENT:
            return self.eventprofile
        else:
            return None

    
    def get_absolute_url(self):
        if self.user_type == SpkrbarUser.USER_TYPE_SPEAKER:
            return self.speakerprofile.get_absolute_url()
        elif self.user_type == SpkrbarUser.USER_TYPE_ATTENDEE:
            return self.attendeeprofile.get_absolute_url()
        elif self.user_type == SpkrbarUser.USER_TYPE_EVENT:
            return self.eventprofile.get_absolute_url()
        else:
            return "/"

    class Meta:
        app_label = 'core'
