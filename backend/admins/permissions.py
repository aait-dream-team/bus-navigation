from rest_framework import permissions
from rest_framework.authtoken.models import Token

from admins.models import Admin

class IsSelfOrSystemAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return "sys-admin" in request.user.user_type