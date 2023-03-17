from django.db import models
from agencies.models import Agency

class StopTime(models.Model):
    arrival_time = models.TimeField()
    departure_time = models.TimeField()
    stop_sequence = models.IntegerField()
    stop_headsign = models.CharField(max_length=200)
    agency = models.ForeignKey(to = Agency, on_delete=models.CASCADE) 
