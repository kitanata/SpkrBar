from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.db import models

class SpkrbarUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()

        if not email:
            raise ValueError('The given email must be set')

        email = SpkrbarUserManager.normalize_email(email)

        user = self.model(email=email,
                          is_staff=False, is_active=True, is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        u = self.create_user(email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


class SpkrbarUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    full_name = models.CharField(max_length=300)

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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = SpkrbarUserManager()

    def get_full_name(self):
        return unicode(self.full_name)

    def get_short_name(self):
        return unicode(self.full_name)

    def get_absolute_url(self):
        return "/profile/" + str(self.pk)

    def __unicode__(self):
        return self.get_full_name()

    class Meta:
        app_label = 'core'
