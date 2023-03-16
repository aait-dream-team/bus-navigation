from rest_framework import permissions
from rest_framework.authtoken.models import Token

from admins.models import Admin

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.agency.admin == request.user