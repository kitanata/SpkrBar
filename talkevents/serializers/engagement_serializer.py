from rest_framework import serializers

from talkevents.models import TalkEvent

class EngagementSerializer(serializers.ModelSerializer):
    abstract = serializers.Field(source='talk.abstract')
    date = serializers.Field(source='formatted_date')
    time = serializers.Field(source='formatted_time')
    talk_url = serializers.Field(source='talk.get_absolute_url')
    talk_name = serializers.Field(source='talk.name')
    event_url = serializers.Field(source='event.get_absolute_url')
    event_name = serializers.Field(source='event.__str__')
    speaker_name = serializers.Field(source='talk.speaker.user.get_full_name')
    city = serializers.Field(source='event.location.city')
    state = serializers.Field(source='event.location.state')
    tags = serializers.Field(source='talk.tags.all')

    class Meta:
        model = TalkEvent
        fields = (
                'id', 
                'abstract',
                'date', 
                'time',
                'talk_url',
                'talk_name',
                'event_url',
                'event_name',
                'speaker_name',
                'tags',
                'city',
                'state',
                'talk', 
                'event', 
                'from_speaker', 
                'vetoed')
