from rest_framework import serializers
from .models import Calendar
class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = ['id', "monday", 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 
                'start_date', 'end_date', 'agency']
        
class ExportCalendarSerializer(serializers.ModelSerializer):
    service_id = serializers.CharField(source='id')
    class Meta:
        model = Calendar
        fields = ['service_id', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'start_date', 'end_date']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return [value for value in data.values()]