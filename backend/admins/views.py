from admins.models import Admin
from admins.serializers import AdminSerializer, CreateAdminSerializer
from rest_framework import permissions
from admins.permissions import IsSystemAdmin
from rest_framework import viewsets, mixins
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

class AdminsViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer

class AdminsCreateViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    queryset = Admin.objects.all()
    serializer_class = CreateAdminSerializer
    permission_classes = [permissions.IsAuthenticated&IsSystemAdmin]