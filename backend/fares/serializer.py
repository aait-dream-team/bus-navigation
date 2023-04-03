from rest_framework import serializers
from .models import Fare
class FareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fare
        fields = ['id', 'price', 'agency', 'route', 'start_stop', 'end_stop']

class ExportFareSerializer(serializers.ModelSerializer):
    fare_id = serializers.CharField(source='id')
    route_id = serializers.CharField(source='route.id')
    origin_id = serializers.CharField(source='start_stop.id')
    destination_id = serializers.CharField(source='end_stop.id')
    contains_id = serializers.CharField(default='')

    class Meta:
        model = Fare
        fields = ['fare_id', 'route_id', 'origin_id', 'destination_id', 'contains_id']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return [value for value in data.values()]
