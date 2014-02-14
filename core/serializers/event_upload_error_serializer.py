from rest_framework import serializers

from core.models import EventUploadError

class EventUploadErrorSerializer(serializers.ModelSerializer):
    description = serializers.Field(source='__str__')

    class Meta:
        model = EventUploadError
        fields = (
                'id', 
                'description',
                )
