from rest_framework import serializers
from .models import Route
class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['id', "route_short_name", 'route_long_name', 'route_desc', 'route_type', 'route_color', 'agency']
