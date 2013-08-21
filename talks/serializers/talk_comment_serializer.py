from rest_framework import serializers

from talks.models import TalkComment

class TalkCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TalkComment
        fields = ('id','talk','comment')
        depth=5
