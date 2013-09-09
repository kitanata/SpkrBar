from rest_framework import serializers

from talks.models import TalkSlideDeck

class TalkSlideDeckSerializer(serializers.ModelSerializer):
    embed_code = serializers.Field(source="build_embed_code")

    class Meta:
        model = TalkSlideDeck
        fields = (
            'id',
            'source',
            'embed_data',
            'aspect',
            'embed_code')
