from rest_framework import serializers

from talks.models import Talk

class TalkSerializer(serializers.ModelSerializer):
    user = serializers.Field(source="speaker.user.pk")

    class Meta:
        model = Talk
        fields = (
                'id', 
                'speaker',
                'user',
                'name', 
                'abstract', 
                'published', 
                'tags', 
                'engagements',
                'endorsements')
