from rest_framework import serializers

from core.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    name = serializers.RelatedField(source='user.get_full_name')
    datetime = serializers.DateTimeField(format="%B %m, %Y at %I:%M %p")
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Comment
        fields = (
            'id',
            'user',
            'name',
            'comment',
            'children',
            'datetime',
            )
