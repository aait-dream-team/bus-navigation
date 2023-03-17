from django.db import models
from agencies.models import Agency


class Fare(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=10)
    agency = models.ForeignKey(to = Agency, on_delete=models.CASCADE) 
