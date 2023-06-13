from rest_framework import serializers
from .models import Alert, VehicleUpdate

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ['affected_entity', 'cause', 'effect', 'duration', 'start_timestamp', 'agency_id', 'route_id', 'trip_id', 'message', 'alert_feed_id']

class VehicleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleUpdate
        fields = ['lat', 'long', 'trip', 'timestamp']