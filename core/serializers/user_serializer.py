from rest_framework import serializers

from core.models import SpkrbarUser, Notification
from notification_serializer import NotificationSerializer

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.Field(source='get_full_name')
    is_speaker = serializers.Field(source='is_speaker')
    is_attendee = serializers.Field(source='is_attendee')
    is_event_planner = serializers.Field(source='is_event_planner')

    class Meta:
        model = SpkrbarUser
        fields = (
                'id', 
                'username', 
                'full_name',
                'email', 
                'following', 
                'followers',
                'is_speaker',
                'is_attendee',
                'is_event_planner',
                )
