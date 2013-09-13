from rest_framework import serializers

from talks.models import Talk, TalkSlideDeck
from core.serializers import UserSerializer
from talk_slide_deck_serializer import TalkSlideDeckSerializer
from talk_video_serializer import TalkVideoSerializer
from talk_photo_serializer import TalkPhotoSerializer
from talk_comment_serializer import TalkCommentSerializer

class TalkSerializer(serializers.ModelSerializer):
    speaker = UserSerializer()
    slides = TalkSlideDeckSerializer()
    videos = TalkVideoSerializer()
    photos = TalkPhotoSerializer()
    comments = TalkCommentSerializer()

    class Meta:
        model = Talk
        fields = (
                'id', 
                'speaker',
                'name', 
                'abstract', 
                'published', 
                'tags', 
                'slides',
                'videos',
                'photos',
                'comments',
                'engagements',
                'endorsements')
