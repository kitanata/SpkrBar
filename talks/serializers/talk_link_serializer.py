from rest_framework import serializers

from talks.models import TalkLink

class TalkLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = TalkLink
        fields = ('id','talk','name', 'url')
