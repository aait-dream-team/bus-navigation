from rest_framework import serializers

from .models import StopTime

class StopTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StopTime
        fields = ['id', 'arrival_time', 'departure_time', 'stop_sequence', 'stop_headsign', 'agency', 'trip', 'stop']

class ExportStopTimeSerializer(serializers.ModelSerializer):
    trip_id = serializers.CharField(source='trip.id')
    arrival_time = serializers.TimeField(source='arrival_time')
    departure_time = serializers.TimeField(source='departure_time')
    stop_id = serializers.CharField(source='stop.id')
    stop_sequence = serializers.IntegerField(source='stop_sequence')
    pickup_type = serializers.CharField(default='')
    drop_off_type = serializers.CharField(default='')

    class Meta:
        model = StopTime
        fields = ['trip_id', 'arrival_time', 'departure_time', 'stop_id', 'stop_sequence', 'pickup_type', 'drop_off_type']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return [value for value in data.values()]
