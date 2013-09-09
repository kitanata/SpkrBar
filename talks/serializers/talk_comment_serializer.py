from rest_framework import serializers

from talks.models import TalkComment

class TalkCommentSerializer(serializers.ModelSerializer):
    commenter = serializers.Field(source="commenter.get_full_name")

    class Meta:
        model = TalkComment
        fields = (
            'id',
            'commenter',
            'comment',
            'datetime')
