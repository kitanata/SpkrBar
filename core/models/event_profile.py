from django.db import models

class EventProfile(models.Model):
    user = models.OneToOneField('SpkrbarUser')
    name = models.CharField(max_length=140)
    description = models.CharField(max_length=800)
    photo = models.ImageField(upload_to="photo")

    tags = models.ManyToManyField('core.ProfileTag')

    def get_absolute_url(self):
        return "/profile/" + self.user.username

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        app_label = 'core'
