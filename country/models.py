from django.db import models

# Create your models here.
class Country(models.Model):
    name_common = models.CharField(max_length=255)
    name_official = models.CharField(max_length=255)
    native_name_common = models.CharField(max_length=255, null=True, blank=True)
    native_name_official = models.CharField(max_length=255, null=True, blank=True)
    
    flags_png = models.URLField(max_length=500)
    flags_svg = models.URLField(max_length=500)
    flags_alt = models.TextField(null=True, blank=True)
    
    capital = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    area = models.FloatField()
    population = models.BigIntegerField()
    
    timezone = models.CharField(max_length=255)
    continent = models.CharField(max_length=100)

    def __str__(self):
        return self.name_common

