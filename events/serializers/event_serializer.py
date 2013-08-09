from rest_framework import serializers

from events.models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
                'id', 
                'owner', 
                'name', 
                'location', 
                'start_date', 
                'end_date', 
                'attendees',
                'endorsements',
                )
        depth = 1
