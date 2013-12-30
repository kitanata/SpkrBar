from rest_framework import serializers

from core.models import UserTag

class UserTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTag
        fields = (
                'id', 
                'name', 
                )
