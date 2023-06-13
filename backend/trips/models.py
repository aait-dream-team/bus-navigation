from django.db import models
from agencies.models import Agency
from shapes.models import Shape
from routes.models import Route
import uuid

class Trip(models.Model):
    id = models.CharField(max_length=200, primary_key=True,  default=uuid.uuid4)
    headsign = models.CharField(max_length=200)
    short_name = models.CharField(max_length=200)
    direction = models.BooleanField()
    agency = models.ForeignKey(to = Agency, on_delete=models.CASCADE)
    shape = models.ForeignKey(to = Shape, default=None, on_delete=models.DO_NOTHING)
    route = models.ForeignKey(to = Route, default=None, on_delete=models.CASCADE)


