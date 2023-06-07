from django.contrib import admin
from bus_navigation_backend.new_admins import super_admin_site
from .models import Agency

# Register your models here.

super_admin_site.register(Agency)