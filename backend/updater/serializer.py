from rest_framework import serializers
from .models import Alert, VehicleUpdate

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ['affected_entity', 'entity_id', 'cause', 'effect', 'duration', 'start_timestamp']

class VehicleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleUpdate
        fields = ['lat', 'long', 'trip', 'timestamp']