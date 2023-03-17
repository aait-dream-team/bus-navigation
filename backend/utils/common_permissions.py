from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.agency.admin == request.user

class IsSystemAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return "sys-admin" in request.user.user_type