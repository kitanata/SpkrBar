from rest_framework import serializers

from engagements.models import Engagement

class EngagementSerializer(serializers.ModelSerializer):
    abstract = serializers.Field(source='talk.abstract')
    formatted_date = serializers.Field(source='formatted_date')
    formatted_time = serializers.Field(source='formatted_time')
    talk_url = serializers.Field(source='talk.get_absolute_url')
    talk_name = serializers.Field(source='talk.name')
    event_url = serializers.Field(source='event.get_absolute_url')
    event_name = serializers.Field(source='event.__str__')
    speaker_name = serializers.Field(source='talk.speaker.user.get_full_name')
    city = serializers.Field(source='event.location.city')
    state = serializers.Field(source='event.location.state')
    tags = serializers.Field(source='event.owner.tags.all')
    endorsements = serializers.Field(source='talk.endorsements.all')
    user_id = serializers.Field(source='talk.speaker.user.id')

    class Meta:
        model = Engagement
        fields = (
                'id', 
                'user_id',
                'abstract',
                'formatted_date', 
                'formatted_time',
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
                'date',
                'attendees',
                'endorsements',
                'from_speaker',
                'confirmed')
