from rest_framework import serializers

from engagements.models import Engagement
from locations.serializers import LocationSerializer

class EngagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Engagement
        fields = (
                'id', 
                'updated_at',
                'created_at',
                'event_name',
                'room',
                'date',
                'time',
                'location',
                'talk',
                'speaker')
