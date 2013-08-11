from rest_framework import serializers

from talks.models import Talk

class TalkTagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Talk
        fields = ('tags',)
        depth=1
