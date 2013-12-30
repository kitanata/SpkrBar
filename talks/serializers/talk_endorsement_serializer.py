from rest_framework import serializers

from talks.models import TalkEndorsement

class TalkEndorsementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TalkEndorsement
        fields = (
            'id',
            'talk',
            'user',
            'updated_at',
            'created_at')
