from rest_framework import serializers
from .models import Trip

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ['id', 'headsign', 'short_name', 'direction', 'agency']

class ExportTripSerializer(serializers.ModelSerializer):
    route_id = serializers.CharField(default='')
    service_id = serializers.CharField(default='')
    trip_id = serializers.CharField(source='id')
    trip_headsign = serializers.CharField(source='headsign')
    block_id = serializers.CharField(default='')

    class Meta:
        model = Trip
        fields = ['route_id', 'service_id', 'trip_id', 'trip_headsign', 'block_id']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return [value for value in data.values()]
