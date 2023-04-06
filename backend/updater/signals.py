from django.db.models.signals import post_save
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Alert, VehicleUpdate
from .serializer import AlertSerializer, VehicleUpdateSerializer


def save_alert_profile(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    print('\n\nhi\n\n')
    print(f'{instance.affected_entity}_{instance.entity_id}')
    async_to_sync(channel_layer.group_send)(f'{instance.affected_entity}_{instance.entity_id}', {
        'type': 'notify_update',
        'message': AlertSerializer(instance).data
    })

def save_vehicle_update_profile(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(f'{instance.affected_entity}_{instance.entity_id}', {
        'type': 'notify_update',
        'message': VehicleUpdateSerializer(instance).data
    })


post_save.connect(save_alert_profile, sender=Alert)
post_save.connect(save_vehicle_update_profile, sender=VehicleUpdate)

