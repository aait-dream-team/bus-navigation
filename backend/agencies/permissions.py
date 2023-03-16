from rest_framework import permissions
from rest_framework.authtoken.models import Token

from admins.models import Admin

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print("Got here.", obj.admin, request.user)
        return obj.admin == request.user