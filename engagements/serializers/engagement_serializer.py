from rest_framework import serializers

from engagements.models import Engagement
from rating_serializer import RatingSerializer
from locations.serializers import LocationSerializer

class EngagementSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    ratings = RatingSerializer(many=True)

    class Meta:
        model = Engagement
        fields = (
                'id', 
                'updated_at',
                'created_at',
                'active',
                'event_name',
                'room',
                'date',
                'time',
                'location',
                'ratings')
