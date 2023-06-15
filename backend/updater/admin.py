from bus_navigation_backend.new_admins import admin_site

# Register your models here
# .
from .models import VehicleUpdate, Alert, TripUpdate
admin_site.register(VehicleUpdate)
admin_site.register(Alert)
admin_site.register(TripUpdate)