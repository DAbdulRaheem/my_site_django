from django.db import models

class Mobiles(models.Model):
    title = models.CharField(max_length=255, blank=True)
    brand = models.CharField(max_length=100, blank=False)
    image = models.URLField()  # will store Cloudinary's URL
