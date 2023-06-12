from django.contrib import admin
from .models import TripUpdate, StopTimeEvent, StopTimeUpdate

# Register your models here.
admin.site.register(TripUpdate)
admin.site.register(StopTimeUpdate)
admin.site.register(StopTimeEvent)  