from django.db import models

# Create your models here.
class BlogPost(models.Model):
    name = models.CharField(max_length=300)
    content = models.TextField()
    published = models.BooleanField(default=True)
    date = models.DateTimeField()

    class Meta:
        app_label = 'blog'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/blog/" + str(self.pk)
