from rest_framework import serializers

from talks.models import TalkVideo

class TalkVideoSerializer(serializers.ModelSerializer):
    embed_code = serializers.Field(source="build_embed_code")

    class Meta:
        model = TalkVideo
        fields = (
            'id',
            'source',
            'embed_data',
            'aspect',
            'embed_code')
