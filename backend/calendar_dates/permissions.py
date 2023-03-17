from rest_framework import permissions
from rest_framework.authtoken.models import Token


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.service.agency.admin == request.user