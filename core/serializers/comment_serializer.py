from rest_framework import serializers

from core.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    name = serializers.RelatedField(source='user.get_full_name')
    datetime = serializers.DateTimeField()
    user = serializers.PrimaryKeyRelatedField()
    class Meta:
        model = Comment
        fields = (
            'id',
            'user',
            'name',
            'comment',
            'parent',
            'children',
            'datetime',
            )
