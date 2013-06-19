from django.db import models

class TalkPhoto(models.Model):
    talk = models.ForeignKey(Talk)
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    photo = models.ImageField(upload_to="photo", width_field="width", height_field="height")
