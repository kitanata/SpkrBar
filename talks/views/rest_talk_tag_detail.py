from talks.models import TalkTag
from talks.serializers import TalkTagSerializer
from rest_framework import permissions, viewsets
from core.permissions import IsOwnerOrReadOnly

class TalkTagDetail(viewsets.ModelViewSet):
    queryset = TalkTag.objects.all()
    serializer_class = TalkTagSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, IsOwnerOrReadOnly)
