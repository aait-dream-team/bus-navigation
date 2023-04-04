from rest_framework import serializers
from .models import Transfer
class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ['id', "from_stop", 'to_stop', 'transfer_type', 'min_transfer_time', 'admin']

class ExportTransferSerializer(serializers.ModelSerializer):
    from_stop_id = serializers.CharField(source='from_stop.id')
    to_stop_id = serializers.CharField(source='to_stop.id')
    transfer_type = serializers.CharField(source='transfer_type')
    min_transfer_time = serializers.CharField(source='min_transfer_time')

    class Meta:
        model = Transfer
        fields = ['from_stop_id', 'to_stop_id', 'transfer_type', 'min_transfer_time']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return [value for value in data.values()]
