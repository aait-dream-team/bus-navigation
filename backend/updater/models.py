from django.db import models
from trips.models import Trip

# Create your models here.
class Update(models.Model):
    pass

class VechicleUpdate(models.Model):
    lat = models.FloatField()
    long = models.FloatField()
    trip = models.ForeignKey(to=Trip, on_delete=models.CASCADE)
    timestamp = models.TimeField()


AFFECTED_ENTITY = (('r', 'route'), ('a', 'agency'), ('t', 'trip'))
CAUSE = ((1, 'UNKNOWN_CAUSE'), (2, 'OTHER_CAUSE'), 
         (3, 'TECHNICAL_PROBLEM'), (4, 'STRIKE'), 
         (5, 'DEMONSTRATION'), (6, 'ACCIDENT'), 
         (7, 'HOLIDAY'), (8, 'WEATHER'), 
         (9, 'MAINTENANCE'), (10, 'CONSTRUCTION'), 
         (11, 'POLICE_ACTIVITY'), (12, 'MEDICAL_EMERGENCY'))

EFFECT = ((1, 'NO_SERVICE'), (2, 'REDUCED_SERVICE'), (3, 'SIGNIFICANT_DELAYS'), 
          (4, 'DETOUR'), (5, 'ADDITIONAL_SERVICE'), (6, 'MODIFIED_SERVICE'), 
          (7, 'OTHER_EFFECT'), (8, 'UNKNOWN_EFFECT'), (9, 'STOP_MOVED'))
class Alert(models.Model):
    affected_entity = models.CharField(choices=CAUSE)
    entity_id = models.UUIDField() 
    cause = models.IntegerField(choices=CAUSE)
    effect = models.IntegerField(choices=EFFECT)
    duration = models.DurationField()
    start_timestamp = models.TimeField()

