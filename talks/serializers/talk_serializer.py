from rest_framework import serializers

from talks.models import Talk, TalkSlideDeck
from core.serializers import UserSerializer
from talk_slide_deck_serializer import TalkSlideDeckSerializer
from talk_video_serializer import TalkVideoSerializer
from talk_comment_serializer import TalkCommentSerializer

class TalkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Talk
        fields = (
                'id', 
                'speaker',
                'created_at',
                'updated_at',
                'name', 
                'abstract', 
                'published', 
                'tags', 
                'links',
                'slides',
                'videos',
                'comments',
                'engagements',
                'endorsements')
