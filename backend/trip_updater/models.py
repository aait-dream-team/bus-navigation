from datetime import datetime
import uuid
from django.db import models
from trips.models import Trip
from routes.models import Route
from agencies.models import Agency
from django.core.exceptions import ValidationError

class VehicleUpdate(models.Model):
    lat = models.FloatField()
    long = models.FloatField()
    trip = models.ForeignKey(to=Trip, on_delete=models.CASCADE)
    timestamp = models.TimeField()


AFFECTED_ENTITY = (('route', 'route'), ('agency', 'agency'), ('trip', 'trip'))
CAUSE = ((1, 'UNKNOWN_CAUSE'), (2, 'OTHER_CAUSE'), 
         (3, 'TECHNICAL_PROBLEM'), (4, 'STRIKE'), 
         (5, 'DEMONSTRATION'), (6, 'ACCIDENT'), 
         (7, 'HOLIDAY'), (8, 'WEATHER'), 
         (9, 'MAINTENANCE'), (10, 'CONSTRUCTION'), 
         (11, 'POLICE_ACTIVITY'), (12, 'MEDICAL_EMERGENCY'))
EFFECT = ((1, 'NO_SERVICE'), (2, 'REDUCED_SERVICE'), (3, 'SIGNIFICANT_DELAYS'), 
          (4, 'DETOUR'), (5, 'ADDITIONAL_SERVICE'), (6, 'MODIFIED_SERVICE'), 
          (7, 'OTHER_EFFECT'), (8, 'UNKNOWN_EFFECT'), (9, 'STOP_MOVED'))

SCHEDULE_RELATIONSHIP = ((0, 'SCHEDULED'), (1, 'SKIPPED'), (2, 'NO_DATA'))
SCHEDULE_RELATIONSHIP_TRIP = ((0, 'SCHEDULED'), (1, 'ADDED'), (2, 'UNSCHEDULED'), (3, 'CANCELED'))

class TripUpdate(models.Model):
    trip_id = models.CharField(max_length=200, unique=True, editable=False)
    route_id = models.CharField(max_length=100)
    start_date = models.DateField()
    start_time = models.TimeField()
    schedule_relationship = models.IntegerField(choices=SCHEDULE_RELATIONSHIP_TRIP)
    stop_time_update = models.ForeignKey(to='StopTimeUpdate', on_delete=models.CASCADE, related_name='stop_time_update', blank=True, null=True)
    

class StopTimeUpdate(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    stop_sequence = models.IntegerField()
    stop_id = models.CharField(max_length=100)
    arrival = models.ForeignKey(to='StopTimeEvent', on_delete=models.CASCADE, related_name='arrival', blank=True, null=True)
    departure = models.ForeignKey(to='StopTimeEvent', on_delete=models.CASCADE, related_name='departure', blank=True, null=True)
    schedule_relationship = models.IntegerField(choices=SCHEDULE_RELATIONSHIP , blank=True, null=True)


class StopTimeEvent(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    delay = models.DurationField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    uncertainty = models.DurationField(null=True, blank=True)

    def clean(self):
        if not (self.delay or self.time or self.uncertainty):
            raise ValidationError(f'At least one field is required. [{self.delay}, {self.time}, {self.uncertainty}]')
    