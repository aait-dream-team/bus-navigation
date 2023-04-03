from rest_framework import serializers
from .models import Agency
class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = ['id', "name", 'url', 'lang', 'time_zone', 'phone', 'admin']

class ExportAgencySerializer(serializers.ModelSerializer):
    agency_id = serializers.CharField(source='id')
    agency_name = serializers.CharField(source='name')
    agency_url = serializers.CharField(source='url')
    agency_timezone = serializers.CharField(source='time_zone')
    agency_phone = serializers.CharField(source='phone')
    agency_lang = serializers.CharField(source='lang')
    
    class Meta:
        model = Agency
        fields = ['agency_id', 'agency_name', 'agency_url', 'agency_timezone', 'agency_phone', 'agency_lang']
    
    def to_representation(self, instance):
        return [value for value in super().to_representation(instance).values()]