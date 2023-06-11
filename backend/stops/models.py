from django.db import models
from admins.models import Admin 

class Stop(models.Model):
    id = models.CharField(max_length=200, primary_key=True,  default=uuid.uuid4)
    stop_name = models.CharField(max_length=200)
    stop_desc = models.CharField(max_length=500)
    stop_code = models.CharField(max_length=50)
    stop_lat = models.CharField(max_length=50)
    stop_long = models.CharField(max_length=50)
    # zone_id = models.CharField(max_length=50)
    stop_url = models.URLField()
    parent_station = models.ForeignKey('stops.Stop', null=True, blank=True, on_delete=models.SET_NULL)

    admin = models.ForeignKey(to = Admin, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.stop_name} ID : {self.id}'

    

