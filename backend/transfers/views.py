# from admins.serializers import AdminSerializer, CreateAdminSerializer
from rest_framework import permissions
from rest_framework import viewsets
from .serializer import TransferSerializer
from stops.permissions import IsOwner
from .models import Transfer

class TransferViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer

    def get_permissions(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            permission_classes = [IsOwner]
        elif self.request.method == 'POST':
            permission_classes = [IsOwner]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
