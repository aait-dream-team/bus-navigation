from rest_framework import permissions
from rest_framework import viewsets
from .serializer import CalendarDateSerializer
from .permissions import IsOwner
from .models import CalendarDate

class CalendarDateViewSet(viewsets.ModelViewSet):
    queryset = CalendarDate.objects.all()
    serializer_class = CalendarDateSerializer

    def get_permissions(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            permission_classes = [IsOwner]
        elif self.request.method == 'POST':
            permission_classes = [IsOwner]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
