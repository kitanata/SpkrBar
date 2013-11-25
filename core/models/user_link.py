from django.db import models

class UserLink(models.Model):
    user = models.ForeignKey('core.SpkrbarUser', related_name='links')

    FACEBOOK = 'FAC'
    TWITTER = 'TWI'
    LINKEDIN = 'LIN'
    LANYRD = 'LAN'
    GITHUB = 'GIT'
    BLOG = 'BLO'
    WEBSITE = 'WEB'

    LINK_TYPE_CHOICES = (
        (FACEBOOK, 'Facebook'),
        (TWITTER, 'Twitter'),
        (LINKEDIN, 'LinkedIn'),
        (LANYRD, 'Lanyrd'),
        (GITHUB, 'GitHub'),
        (BLOG, 'Blog'),
        (WEBSITE, 'Other Website'),
    )

    type_name = models.CharField(max_length=40, choices=LINK_TYPE_CHOICES, default=TWITTER)
    other_name = models.CharField(max_length=100, default="Other Website")
    url_target = models.URLField(max_length=140)

    def __str__(self):
        return self.type_name

    class Meta:
        app_label = 'core'
