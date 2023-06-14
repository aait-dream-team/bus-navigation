from django.db import models
from agencies.models import Agency

class Trip(models.Model):
    headsign = models.CharField(max_length=200)
    short_name = models.CharField(max_length=200)
    direction = models.BooleanField()
    agency = models.ForeignKey(to = Agency, on_delete=models.CASCADE) 


