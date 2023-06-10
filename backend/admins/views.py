from datetime import timedelta, datetime
import pytz
from admins.models import Admin
from admins.serializers import AdminSerializer, CreateAdminSerializer
from admins.serializers import ResetRequestSerializer, ResetPasswordSerializer
from rest_framework import permissions
from admins.permissions import IsSystemAdmin
from rest_framework import viewsets, mixins
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes,permission_classes
from django.core.mail import send_mail

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

@api_view(['POST'])
@authentication_classes([])
@permission_classes([permissions.AllowAny])
def reset_request(request):
    serializer = ResetRequestSerializer(data=request.data)
    if serializer.is_valid():
        data = request.data
        email = data['email']
        user = Admin.objects.get(email=email)
        if Admin.objects.filter(email=email).exists():
            user.save() #regenerate new OTP
            # Send OTP
            send_mail("Bus Navigation Password Reset", f"Your password reset OTP Code is {user.otp} \nThe code is valid for 30 minutes.", "bus-nav-verify@bus-nav.com", [email], fail_silently=False)
            message = { 'detail': 'Email Sent Successfully' }
            return JsonResponse(message, status=200)
        else:
            message = {
                'detail': 'Invalid email address'}
            return JsonResponse(message, status=400)
    else:
        message = {'detail': 'Invalid request data'}
        return JsonResponse(message, status=400)
    
@api_view(['PUT'])
@authentication_classes([])
@permission_classes([permissions.AllowAny])
def reset_password(request):
    serializer = ResetPasswordSerializer(data=request.data)
    if serializer.is_valid():
        data = request.data
        user = Admin.objects.get(email=data['email'])
        if user.is_active:
            # Check if otp is valid
            if data['otp'] == user.otp and user.otp_created_at + timedelta(minutes=30) > datetime.now(pytz.timezone('Africa/Addis_Ababa')):
                if data['password'] != '':
                    # Change Password
                    user.set_password(data['password'])
                    user.save() # Here user otp will also be changed on save automatically 
                    return JsonResponse({ 'detail' : 'Password changed successfully'}, status=200)
                else:
                    message = {
                        'detail': 'Password cant be empty'}
                    return JsonResponse(message, status=400)
            else:
                message = {
                    'detail': 'OTP expired, please request a new one'}
                return JsonResponse(message, status=400)
        else:
            message = {
                'detail': 'Something went wrong'}
            return JsonResponse(message, status=400)
    else:
        message = {
            'detail': 'Invalid request data'}
        return JsonResponse(message, status=400)