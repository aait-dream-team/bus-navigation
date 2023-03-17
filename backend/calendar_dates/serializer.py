from rest_framework import serializers
from .models import CalendarDate
class CalendarDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarDate
        fields = ['id', "service", 'date', 'exception_type']


        
