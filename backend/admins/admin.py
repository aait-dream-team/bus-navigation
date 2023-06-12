from bus_navigation_backend.new_admins import super_admin_site
from .models import Admin
# Register your models here.

super_admin_site.register(Admin)