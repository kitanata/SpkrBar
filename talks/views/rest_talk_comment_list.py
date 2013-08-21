from talks.models import TalkComment
from talks.serializers import TalkCommentSerializer
from rest_framework import generics, permissions, viewsets

class TalkCommentList(generics.ListAPIView):
    serializer_class = TalkCommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return TalkComment.objects.filter(talk__pk=self.kwargs['talk_id'])
