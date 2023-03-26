from rest_framework import serializers
from admins.models import Admin, USER_TYPES

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ('id', 'email', 'first_name', 'last_name', 'user_type')
        read_only_fields = ('email', 'user_type')

class CreateAdminSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        # call create_user on user object. Without this
        # the password will be stored in plain text.
        admin = Admin.objects.create_user(**validated_data)
        return admin

    class Meta:
        model = Admin
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email', 'auth_token', 'user_type')
        read_only_fields = ('auth_token',)
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': True}, 
            'user_type': {'required': True},   
        }
