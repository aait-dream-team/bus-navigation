from rest_framework import viewsets, permissions

from trips.serializer import TripSerializer
from utils.common_permissions import IsOwner, IsSystemAdmin
from .models import Trip

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    def get_permissions(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            permission_classes = [IsOwner]
        elif self.request.method == 'POST':
            permission_classes = [IsOwner | IsSystemAdmin]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
