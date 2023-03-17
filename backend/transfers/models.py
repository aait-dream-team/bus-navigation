from django.db import models
from stops.models import Stop
from admins.models import Admin

TransferType = (("dkn" , "don't know"), ("now", 'dont'))

class Transfer(models.Model):
    from_stop = models.ForeignKey(to = Stop , on_delete=models.CASCADE, related_name='from_stops')
    to_stop = models.ForeignKey(to = Stop, on_delete=models.CASCADE , related_name='to_stops')
    transfer_type = models.CharField(choices=TransferType, max_length=100)
    min_transfer_time = models.PositiveIntegerField()
    admin = models.ForeignKey(to = Admin , on_delete=models.CASCADE)

    class Meta:
        unique_together = (('from_stop', 'to_stop'),)
    def __str__(self):
        return f'from {self.from_stop} to {self.to_stop} admin : {self.admin.username}'

    

