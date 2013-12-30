from talks.models import TalkVideo
from talks.serializers import TalkVideoSerializer
from rest_framework import permissions, viewsets
from core.permissions import IsOwnerOrReadOnly

class TalkVideoDetail(viewsets.ModelViewSet):
    queryset = TalkVideo.objects.all()
    serializer_class = TalkVideoSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, IsOwnerOrReadOnly)
