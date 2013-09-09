from django.db import models

class TalkPhoto(models.Model):
    talk = models.ForeignKey('Talk', related_name='photos')
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
    photo = models.ImageField(upload_to="photo", width_field="width", height_field="height")

    class Meta:
        app_label = 'talks'

    def build_html(self):
        aspect = self.width / float(self.height) if self.height != 0 else 0
        width = min(self.width, 200)
        return "<img src='%s' width='%d' height='%d'></img>" % (self.photo.url, width, width * aspect)
