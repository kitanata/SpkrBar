from rest_framework import serializers

from core.models import EventUploadSummary

class EventUploadSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventUploadSummary
        fields = (
                'id', 
                'name',
                'description',
                )
