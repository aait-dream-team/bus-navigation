from rest_framework import serializers
from .models import CalendarDate
class CalendarDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarDate
        fields = ['id', "service", 'date', 'exception_type']


        
class ExportCalendarDateSerializer(serializers.ModelSerializer):
    service_id = serializers.CharField(source='service.id')
    date = serializers.DateField(source='date')
    exception_type = serializers.CharField(source='exception_type')
    
    class Meta:
        model = CalendarDate
        fields = ['service_id', 'date', 'exception_type']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        return [value for value in data.values()]
