from talks.models import TalkLink
from talks.serializers import TalkLinkSerializer
from rest_framework import permissions, viewsets
from core.permissions import IsOwnerOrReadOnly

class TalkLinkDetail(viewsets.ModelViewSet):
    queryset = TalkLink.objects.all()
    serializer_class = TalkLinkSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, IsOwnerOrReadOnly)
