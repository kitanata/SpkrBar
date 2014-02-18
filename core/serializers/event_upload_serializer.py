from rest_framework import serializers

from core.models import EventUpload

class EventUploadSerializer(serializers.ModelSerializer):
    billed = serializers.Field(source='user_billed') #read-only

    class Meta:
        model = EventUpload
        fields = (
                'id', 
                'name',
                'location',
                'user',
                'state',
                'errors',
                'billed'
                )
