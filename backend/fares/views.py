from .models import Fare
from rest_framework import permissions
from admins.permissions import IsSystemAdmin
from rest_framework import viewsets, mixins
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from .serializer import FareSerializer
from admins.permissions import IsSystemAdmin
from utils.common_permissions import IsOwner, IsSystemAdmin

class FareViewSet(viewsets.ModelViewSet):
    queryset = Fare.objects.all()
    serializer_class = FareSerializer

    def get_permissions(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            permission_classes = [permissions.IsAuthenticated & IsOwner]
        elif self.request.method == 'POST':
            permission_classes = [permissions.IsAuthenticated & (IsSystemAdmin | IsOwner)]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
