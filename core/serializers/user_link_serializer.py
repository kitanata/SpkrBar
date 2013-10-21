from rest_framework import serializers

from core.models import UserLink

class UserLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLink
        fields = (
                'id', 
                'user', 
                'type_name',
                'url_target',
                )
