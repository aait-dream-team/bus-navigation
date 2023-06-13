from django.db import models
from agencies.models import Agency
import uuid

RouteType = (("car" , "Roads"),("air", "AirPlanes"))
class Route(models.Model):
    id = models.CharField(max_length=200, primary_key=True, default=uuid.uuid4)
    route_short_name = models.CharField(max_length=200)
    route_long_name = models.CharField(max_length=300)
    route_desc = models.CharField(max_length=500)
    route_type = models.CharField(choices=RouteType, max_length=200) # TODO don't know what route_types are
    route_url = models.URLField()
    route_color = models.CharField(max_length=20)
    route_text_color = models.CharField(max_length=20)
    agency = models.ForeignKey(to = Agency, on_delete=models.CASCADE) 

