from rest_framework import serializers

from .models import StopTime

class StopTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StopTime
        fields = ['id', 'arrival_time', 'departure_time', 'stop_sequence', 'stop_headsign', 'agency', 'trip', 'stop']
