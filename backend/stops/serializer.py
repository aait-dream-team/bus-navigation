from rest_framework import serializers
from .models import Stop
class StopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stop
        fields = ['id', "stop_name", 'stop_desc', 'stop_lat', 'stop_long', 'stop_code', 'stop_url', 'admin', 'parent_station']

class ExportStopSerializer(serializers.ModelSerializer):
    level_id = serializers.CharField(default='')
    parent_station = serializers.CharField(source='parent_station.stop_name', default='')
    stop_id = serializers.CharField(source='id')
    stop_lon = serializers.CharField(source='stop_long')
    class Meta:
        model = Stop
        fields = ['stop_id','level_id', 'stop_name', 'stop_lat', 'stop_lon', 'parent_station']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return [value for value in data.values()]
