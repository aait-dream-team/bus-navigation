from django.db.models.signals import post_save
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Alert, VehicleUpdate
from .serializer import AlertSerializer, VehicleUpdateSerializer


def save_alert_profile(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    print('\n\nhi\n\n')
    if instance.affected_entity == 'trip':
        connection_string = f'{instance.affected_entity}_{instance.trip_id}'    
    elif instance.affected_entity == 'route':
        connection_string = f'{instance.affected_entity}_{instance.route_id}'
    elif instance.affected_entity == 'agency':
        connection_string = f'{instance.affected_entity}_{instance.agency_id}_12121212' 
    connection_string =  "trip_id_12121212" 
    print(connection_string)
    async_to_sync(channel_layer.group_send)(connection_string, {
        'type': 'notify_update',
        'message': AlertSerializer(instance).data
    })

def save_vehicle_update_profile(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    connection_string = f'{instance.affected_entity}_{instance.alert_feed_id}'   
    print(connection_string)
    async_to_sync(channel_layer.group_send)(connection_string, {
        'type': 'notify_update',
        'message': VehicleUpdateSerializer(instance).data
    })


post_save.connect(save_alert_profile, sender=Alert)
post_save.connect(save_vehicle_update_profile, sender=VehicleUpdate)

