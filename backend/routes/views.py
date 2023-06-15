from .models import Route
# from admins.serializers import AdminSerializer, CreateAdminSerializer
from rest_framework import permissions
from rest_framework import viewsets
from .serializer import RouteSerializer
from .permissions import IsOwner

class RouteViewSet(viewsets.ModelViewSet):
    serializer_class = RouteSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == "sys-admin":
            return Route.objects.all()
        else:
            return Route.objects.filter(agency__admin=user)

    def get_permissions(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            permission_classes = [permissions.IsAuthenticated & IsOwner]
        elif self.request.method == 'POST':
            permission_classes = [permissions.IsAuthenticated & IsOwner]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
