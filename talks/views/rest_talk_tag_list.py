from talks.models import TalkTag
from talks.serializers import TalkTagSerializer
from rest_framework import generics, permissions, viewsets

class TalkTagList(generics.ListAPIView):
    serializer_class = TalkTagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return TalkTag.objects.filter(talk__pk=self.kwargs['talk_id'])
