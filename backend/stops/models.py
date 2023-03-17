from django.db import models
from admins.models import Admin 

LocationType = (("dkn" , "don't know"), ("now", 'dont'))
class Stop(models.Model):
    stop_name = models.CharField(max_length=200)
    stop_desc = models.CharField(max_length=500)
    stop_code = models.CharField(max_length=50)
    stop_lat = models.CharField(max_length=50)
    stop_long = models.CharField(max_length=50)
    # zone_id = models.CharField(max_length=50)
    stop_url = models.URLField()
    location_type = models.CharField(choices=LocationType, max_length=100) # TODO don't know what location_types are
    # parent_station = models.ForeignKey('self', on_delete=models.CASCADE, null=True) # TODO recursive problem
    admin = models.ForeignKey(to = Admin, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.stop_name} ID : {self.id}'

    

