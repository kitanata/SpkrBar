from rest_framework import serializers
from core.serializers import CommentSerializer
from talks.models import TalkComment

class TalkCommentSerializer(serializers.ModelSerializer):
    talk = serializers.PrimaryKeyRelatedField()
    comment = serializers.PrimaryKeyRelatedField()
    class Meta:
        model = TalkComment
        fields = ('id','talk','comment')
