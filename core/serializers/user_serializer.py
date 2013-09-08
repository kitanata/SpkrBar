from rest_framework import serializers

from core.models import SpkrbarUser, Notification
from notification_serializer import NotificationSerializer

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.Field(source='get_full_name')

    class Meta:
        model = SpkrbarUser
        fields = (
                'id', 
                'username', 
                'full_name',
                'email', 
                'following', 
                'followers'
                )
