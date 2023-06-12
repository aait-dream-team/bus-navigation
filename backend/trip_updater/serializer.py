from rest_framework import serializers
from .models import TripUpdate, StopTimeEvent, StopTimeUpdate

class StopTimeEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = StopTimeEvent
        fields = ['delay', 'time', 'uncertainty', 'id']
class StopTimeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StopTimeUpdate
        fields = ['stop_sequence', 'stop_id', 'arrival', 'departure', 'schedule_relationship', 'id']
class TripUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripUpdate
        fields = ['trip_id', 'route_id', 'start_date', 'start_time', 'schedule_relationship', 'stop_time_update', 'id']

