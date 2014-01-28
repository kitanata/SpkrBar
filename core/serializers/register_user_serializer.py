from rest_framework import serializers

from core.models import SpkrbarUser

class RegisterUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, min_length=8)
    confirm = serializers.CharField(required=True, min_length=8)
    full_name = serializers.CharField(required=True)
    about_me = serializers.CharField(required=False)
