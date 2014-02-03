from rest_framework import serializers

from core.models import EventUpload

class EventUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventUpload
        fields = (
                'id', 
                'name',
                'location',
                'user',
                'state',
                'user_billed'
                )
