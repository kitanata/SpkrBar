from rest_framework import serializers

from talks.models import Talk

class TalkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Talk
        fields = (
                'id', 
                'speaker', 
                'name', 
                'abstract', 
                'published', 
                'tags', 
                'engagements',
                'endorsements')
