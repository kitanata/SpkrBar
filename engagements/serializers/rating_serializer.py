from rest_framework import serializers

from engagements.models import Rating

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = (
                'id', 
                'created_at',
                'updated_at',
                'engagement',
                'knowledge',
                'professionalism',
                'resources',
                'discussion')
