from rest_framework import serializers

from core.models import SpkrbarUser, Notification
from notification_serializer import NotificationSerializer

class UserSerializer(serializers.ModelSerializer):
    url = serializers.Field(source='get_absolute_url')
    billed = serializers.Field(source='billed_forever') #read-only

    class Meta:
        model = SpkrbarUser
        fields = (
                'id', 
                'is_staff',
                'is_event_manager',
                'plan_name',
                'billed',
                'profile_public',
                'full_name',
                'about_me',
                'url',
                'photo',
                'following', 
                'followers',
                'tags',
                'links',
                'talks',
                'engagements'
                )
