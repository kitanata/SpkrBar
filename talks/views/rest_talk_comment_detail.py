from talks.models import TalkComment
from talks.serializers import TalkCommentSerializer
from rest_framework import permissions, viewsets
from core.permissions import IsOwnerOrReadOnly

class TalkCommentDetail(viewsets.ModelViewSet):
    queryset = TalkComment.objects.all()
    serializer_class = TalkCommentSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, IsOwnerOrReadOnly)
