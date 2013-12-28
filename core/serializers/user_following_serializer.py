from rest_framework import serializers

from core.models import UserFollowing

class UserFollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFollowing
        fields = (
                'id', 
                'user', 
                'following',
                'updated_at',
                'created_at',
                )
