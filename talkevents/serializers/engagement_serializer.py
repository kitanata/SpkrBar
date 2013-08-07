from rest_framework import serializers

from talkevents.models import TalkEvent

class EngagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TalkEvent
        fields = (
                'id', 
                'talk', 
                'event', 
                'date', 
                'attendees', 
                'from_speaker', 
                'vetoed')
