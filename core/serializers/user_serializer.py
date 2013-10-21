from rest_framework import serializers

from core.models import SpkrbarUser, Notification
from notification_serializer import NotificationSerializer

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.Field(source='get_full_name')
    url = serializers.Field(source='get_absolute_url')

    class Meta:
        model = SpkrbarUser
        fields = (
                'id', 
                'username', 
                'full_name',
                'first_name',
                'last_name',
                'about_me',
                'url',
                'photo',
                'email', 
                'following', 
                'followers',
                'tags',
                'links'
                )
