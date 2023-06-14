from django.db import models
from agencies.models import Agency

class Calendar(models.Model):
    service_id = models.CharField(max_length=200, default='default')
    monday = models.BooleanField()
    tuesday = models.BooleanField()
    wednesday = models.BooleanField()
    thursday = models.BooleanField()
    friday = models.BooleanField()
    saturday = models.BooleanField()
    sunday = models.BooleanField()
    start_date = models.DateField()
    end_date = models.DateField()
    agency = models.ForeignKey(to = Agency, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = (('agency', 'start_date'),)

    def __str__(self):
        return f'{self.agency.name} ID : {self.id} date : {self.start_date} - {self.end_date}'
    

    

