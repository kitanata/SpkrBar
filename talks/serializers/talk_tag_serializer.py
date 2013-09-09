from rest_framework import serializers

from talks.models import TalkTag

class TalkTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TalkTag
        fields = ('id','name')
