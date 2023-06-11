from bus_navigation_backend.new_admins import admin_site

# Register your models here
# .
from .models import VehicleUpdate, Alert
admin_site.register(VehicleUpdate)
admin_site.register(Alert)
