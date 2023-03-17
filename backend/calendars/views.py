# Create your views here.
# from admins.serializers import AdminSerializer, CreateAdminSerializer
from rest_framework import permissions
from rest_framework import viewsets
from .serializer import CalendarSerializer
from routes.permissions import IsOwner
from .models import Calendar

class CalendarViewSet(viewsets.ModelViewSet):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer

    def get_permissions(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            permission_classes = [IsOwner]
        elif self.request.method == 'POST':
            permission_classes = [IsOwner]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
