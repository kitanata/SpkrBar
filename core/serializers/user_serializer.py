from rest_framework import serializers

from core.models import SpkrbarUser, Notification
from notification_serializer import NotificationSerializer

class UserSerializer(serializers.ModelSerializer):
    url = serializers.Field(source='get_absolute_url')

    class Meta:
        model = SpkrbarUser
        fields = (
                'id', 
                'username', 
                'first_name',
                'last_name',
                'about_me',
                'url',
                'photo',
                'email', 
                'following', 
                'followers',
                'tags',
                'links',
                'talks',
                'engagements'
                )
