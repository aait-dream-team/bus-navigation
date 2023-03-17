from rest_framework import serializers
from .models import Calendar
class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = ['id', "monday", 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 
                'start_date', 'end_date', 'agency']
        
