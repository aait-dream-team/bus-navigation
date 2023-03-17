from rest_framework import serializers
from .models import Transfer
class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ['id', "from_stop", 'to_stop', 'transfer_type', 'min_transfer_time', 'admin']

