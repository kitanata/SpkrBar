from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=140)
    address = models.CharField(max_length=140)
    city = models.CharField(max_length=140)
    state = models.CharField(max_length=140)
    zip_code = models.CharField(max_length=9)

    class Meta:
        app_label = 'locations'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/location/" + str(self.pk)

    def form_str(self):
        return self.name + " - " + self.city + ", " + self.state

    def geocode_querystring(self):
        strings = (
            self.address.replace(' ', '%20'),
            self.city.replace(' ', '%20'),
            self.state.replace(' ', '%20'),
            self.zip_code.strip()
            )

        return ','.join(strings)

    def geocode_city_querystring(self):
        strings = (
            self.city.replace(' ', '%20'),
            self.state.replace(' ', '%20'),
            self.zip_code.strip()
            )

        return ','.join(strings)

