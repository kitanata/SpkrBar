from django.db import models

class UserLink(models.Model):
    user = models.ForeignKey('core.SpkrbarUser', related_name='links')

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

    def __str__(self):
        return self.type_name


    class Meta:
        app_label = 'core'
