from .models import Agency
from rest_framework import permissions
from admins.permissions import IsSystemAdmin
from rest_framework import viewsets
from .serializer import AgencySerializer
from admins.permissions import IsSystemAdmin
from .permissions import IsOwner
from rest_framework.decorators import api_view, authentication_classes,permission_classes

@authentication_classes([])
@permission_classes([permissions.AllowAny])
class AgencyViewSet(viewsets.ModelViewSet):
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer

    # def get_permissions(self):
    #     if self.request.method == 'PUT' or self.request.method == 'PATCH':
    #         permission_classes = [permissions.IsAuthenticated & IsOwner]
    #     elif self.request.method == 'POST':
    #         permission_classes = [permissions.IsAuthenticated & IsSystemAdmin]
    #     else:
    #         permission_classes = [permissions.IsAuthenticated]
    #     return [permission() for permission in permission_classes]
