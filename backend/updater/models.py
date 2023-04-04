from django.db import models
from trips.models import Trip

from django.db.models.signals import post_save
from channels.layers import get_channel_layer


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
class Alert(models.Model):
    affected_entity = models.CharField(choices=AFFECTED_ENTITY, max_length=40)
    entity_id = models.UUIDField() 
    cause = models.IntegerField(choices=CAUSE)
    effect = models.IntegerField(choices=EFFECT)
    duration = models.DurationField()
    start_timestamp = models.TimeField()


def save_alert_profile(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    print('\n\nhi\n\n')
    print(f'{instance.affected_entity}_{instance.entity_id}')
    channel_layer.send(f'{instance.affected_entity}_{instance.entity_id}', {
        'type': 'notify_update',
        'message': instance
    })

def save_vehicle_update_profile(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    channel_layer.send(f'trip_{instance.trip.id}', {
        'type': 'notify_update',
        'message': instance    
    })


post_save.connect(save_alert_profile, sender=Alert)
post_save.connect(save_vehicle_update_profile, sender=VehicleUpdate)

