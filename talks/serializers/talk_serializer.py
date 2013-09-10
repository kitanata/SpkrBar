from rest_framework import serializers

from talks.models import Talk, TalkSlideDeck
from talk_slide_deck_serializer import TalkSlideDeckSerializer
from talk_video_serializer import TalkVideoSerializer
from talk_photo_serializer import TalkPhotoSerializer
from talk_comment_serializer import TalkCommentSerializer

class TalkSerializer(serializers.ModelSerializer):
    user = serializers.Field(source="speaker.pk")
    photo = serializers.ImageField(source="speaker.photo")
    speaker = serializers.Field(source="speaker.get_full_name")
    speaker_url = serializers.Field(source="speaker.get_absolute_url")
    slides = TalkSlideDeckSerializer()
    videos = TalkVideoSerializer()
    photos = TalkPhotoSerializer()
    comments = TalkCommentSerializer()

    class Meta:
        model = Talk
        fields = (
                'id', 
                'user',
                'speaker',
                'speaker_url',
                'name', 
                'abstract', 
                'photo',
                'published', 
                'tags', 
                'slides',
                'videos',
                'photos',
                'comments',
                'engagements',
                'endorsements')
