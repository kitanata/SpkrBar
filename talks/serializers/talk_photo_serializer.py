from rest_framework import serializers

from talks.models import TalkPhoto

class TalkPhotoSerializer(serializers.ModelSerializer):
    html_code = serializers.Field(source="build_html")

    class Meta:
        model = TalkPhoto
        fields = (
            'id',
            'width',
            'height',
            'photo',
            'html_code')
