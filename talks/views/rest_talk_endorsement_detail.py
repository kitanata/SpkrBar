from talks.models import TalkEndorsement
from talks.serializers import TalkEndorsementSerializer
from rest_framework import permissions, viewsets
from core.permissions import IsOwnerOrReadOnly

class TalkEndorsementDetail(viewsets.ModelViewSet):
    queryset = TalkEndorsement.objects.all()
    serializer_class = TalkEndorsementSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, IsOwnerOrReadOnly)
