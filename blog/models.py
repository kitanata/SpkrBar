from django.db import models
from tinymce.models import HTMLField

# Create your models here.
class BlogPost(models.Model):
    name = models.CharField(max_length=300)
    content = HTMLField()
    published = models.BooleanField(default=True)
    date = models.DateTimeField()

    def __str__(self):
        return self.name
