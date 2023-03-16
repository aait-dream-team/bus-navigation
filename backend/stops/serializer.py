from rest_framework import serializers
from .models import Stop
class StopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stop
        fields = ['id', "stop_name", 'stop_desc', 'stop_lat', 'stop_long', 'stop_code', 'stop_url', 'location_type', 'admin']
