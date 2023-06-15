from rest_framework import serializers
from .models import Alert, VehicleUpdate

class AlertSerializer(serializers.ModelSerializer):
    cause = serializers.SerializerMethodField()
    effect = serializers.SerializerMethodField()
    class Meta:
        model = Alert
        fields = ['affected_entity', 'cause', 'effect', 'duration', 'start_timestamp', 'agency_id', 'route_id', 'trip_id', 'message', 'alert_feed_id']
    
    def get_cause(self, obj):
        return obj.get_cause_display()
    
    def get_effect(self, obj):
        return obj.get_effect_display()

class VehicleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleUpdate
        fields = ['lat', 'long', 'trip', 'timestamp']