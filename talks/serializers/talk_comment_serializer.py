from rest_framework import serializers
from core.serializers import CommentSerializer
from talks.models import TalkComment

class TalkCommentSerializer(serializers.ModelSerializer):
    talk = serializers.PrimaryKeyRelatedField(read_only=True)
    comment = CommentSerializer()
    class Meta:
        model = TalkComment
        fields = ('id','talk','comment')
        depth=5
