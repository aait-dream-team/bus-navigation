from django.db import models
from agencies.models import Agency
from stops.models import Stop
from trips.models import Trip

class StopTime(models.Model):
    arrival_time = models.TimeField()
    departure_time = models.TimeField()
    stop_sequence = models.IntegerField()
    stop_headsign = models.CharField(max_length=200)
    agency = models.ForeignKey(to = Agency, on_delete=models.CASCADE) 
    trip = models.ForeignKey(to = Trip, on_delete=models.CASCADE)
    stop = models.ForeignKey(to = Stop, on_delete=models.CASCADE)
    timepoint = models.IntegerField(default=0)

    class Meta:
        unique_together = (('trip', 'stop_sequence'),)