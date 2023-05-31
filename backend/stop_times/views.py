from rest_framework import viewsets, permissions
from stop_times.models import StopTime
from stop_times.serializer import StopTimeSerializer
from utils.common_permissions import IsOwner, IsSystemAdmin


class StopTimeViewSet(viewsets.ModelViewSet):
    queryset = StopTime.objects.all()
    serializer_class = StopTimeSerializer

    def get_permissions(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            permission_classes = [permissions.IsAuthenticated & IsOwner]
        elif self.request.method == 'POST':
            permission_classes = [permissions.IsAuthenticated & (IsOwner | IsSystemAdmin)]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
