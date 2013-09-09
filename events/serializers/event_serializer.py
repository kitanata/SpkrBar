from rest_framework import serializers

from events.models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
                'id', 
                'updated_at',
                'created_at',
                'name', 
                'year',
                'location', 
                )
        depth = 1
