from rest_framework import serializers
from .models import Route
class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['id', "route_short_name", 'route_long_name', 'route_desc', 'route_type', 'route_color', 'agency']

class ExportRouteSerializer(serializers.ModelSerializer):
    route_id = serializers.CharField(source='id')
    route_short_name = serializers.CharField(source='route_short_name')
    route_long_name = serializers.CharField(source='route_long_name')
    route_desc = serializers.CharField(default='')
    route_type = serializers.CharField(source='route_type')

    class Meta:
        model = Route
        fields = ['route_id', 'route_short_name', 'route_long_name', 'route_desc', 'route_type']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return [value for value in data.values()]
