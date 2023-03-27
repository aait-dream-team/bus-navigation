from rest_framework import serializers
from .models import Fare
class FareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fare
        fields = ['id', 'price', 'agency', 'route', 'start_stop', 'end_stop']
