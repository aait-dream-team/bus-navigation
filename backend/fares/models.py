from django.db import models
from agencies.models import Agency
from routes.models import Route
from stops.models import Stop


class Fare(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=10)
    agency = models.ForeignKey(to = Agency, on_delete=models.CASCADE) 
    route = models.ForeignKey(to = Route, on_delete=models.CASCADE)
    start_stop = models.ForeignKey(to=Stop, on_delete=models.CASCADE, related_name='start_stops')
    end_stop = models.ForeignKey(to=Stop, on_delete=models.CASCADE, related_name='end_stops')
