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
    # trip = models.ForeignKey(to=Trip, on_delete=models.CASCADE)
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




class Alert(models.Model):
    alert_feed_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    affected_entity = models.CharField(choices=AFFECTED_ENTITY, max_length=40)
    # entity_id = models.UUIDField() 
    cause = models.IntegerField(choices=CAUSE)
    effect = models.IntegerField(choices=EFFECT)
    duration = models.DurationField()
    start_timestamp = models.DateTimeField(default=datetime.now)
    agency_id = models.ForeignKey(to=Agency, on_delete=models.CASCADE, blank=True, null=True)
    route_id = models.ForeignKey(to=Route, on_delete=models.CASCADE, blank=True, null=True)
    trip_id = models.ForeignKey(to=Trip, on_delete=models.CASCADE, blank=True, null=True)
    message = models.CharField(max_length=2000, blank=True, null=True)

    def clean(self):
        if not (self.agency_id or self.route_id or self.trip_id):
            raise ValidationError('At least one field is required.')