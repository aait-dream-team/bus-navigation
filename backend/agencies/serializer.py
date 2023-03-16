from rest_framework import serializers
from .models import Agency
class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = ['id', "name", 'url', 'lang', 'time_zone', 'phone', 'admin']