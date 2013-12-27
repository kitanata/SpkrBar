from talks.models import TalkComment
from talks.serializers import TalkCommentSerializer
from rest_framework import permissions, generics
from core.permissions import IsOwnerOrReadOnly

class TalkCommentList(generics.ListAPIView):
    queryset = TalkComment.objects.all()
    serializer_class = TalkCommentSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, IsOwnerOrReadOnly)

    def get_queryset(self):
        return TalkComment.objects.filter(talk__id=self.kwargs['talk_id'])