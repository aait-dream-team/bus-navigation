from django.contrib import admin

class AdminSite(admin.AdminSite):
    site_header = "Bus Navigation Admin"
    site_title = "Bus Navigation Admin Portal"
    index_title = "Welcome to Bus Navigation Admin Portal"

class SuperAdminSite(admin.AdminSite):
    site_header = "Bus Navigation Super Admin"
    site_title = "Bus Navigation Super Admin Portal"
    index_title = "Welcome to Bus Navigation Super Admin Portal"

super_admin_site = SuperAdminSite(name='super_admin')
admin_site = admin.AdminSite(name='admin')