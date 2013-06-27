from django.contrib.auth.models import AbstractBaseUser
from django.db import models

class SpkrbarBaseUser(AbstractBaseUser):
    username = models.CharField(max_length=30)
    email = models.EmailField()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    def get_full_name(self):
        return str(self.username)

    def get_short_name(self):
        return str(self.username)

    class Meta:
        app_label = 'core'
