from user.models import User
from rest_framework import serializers
from oauth2_provider.models import AccessToken
from rest_framework.permissions import BasePermission


class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    auth_type = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password',
                  'first_name', 'last_name', 'auth_type')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class CustomTokenSerializer(serializers.ModelSerializer):
    """ Used when a user logs in manually """

    user = serializers.SerializerMethodField()

    class Meta:
        model = AccessToken
        fields = ('expires', 'scope', 'user')

    def get_user(self, obj):
        user_data = obj.user
        return {
            'id': user_data.id,
            'email': user_data.email,
            'username': user_data.username,
            'first_name': user_data.first_name,
            'last_name': user_data.last_name,
            'auth_type': user_data.auth_type,
            'is_staff': user_data.is_staff
        }


class IsSuperUser(BasePermission):
    """ Custom permission to only allow superusers to access the endpoint. """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superuser
