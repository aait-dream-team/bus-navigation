from rest_framework import permissions
from rest_framework.authtoken.models import Token

from admins.models import Admin

class IsSystemAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return "sys-admin" in request.user.user_type