from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.db import models

class SpkrbarUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField()

    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)

    about_me = models.CharField(max_length=4000, blank=True)

    photo = models.ImageField(upload_to="photo", blank=True)

    tags = models.ManyToManyField('core.UserTag', blank=True)

    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    following = models.ManyToManyField('self', 
            related_name="followers", symmetrical=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def get_full_name(self):
        return u' '.join([unicode(self.first_name), unicode(self.last_name)])

    def get_short_name(self):
        return unicode(self.first_name)

    def get_absolute_url(self):
        return "/profile/" + self.username

    def __unicode__(self):
        return self.get_full_name()

    class Meta:
        app_label = 'core'
