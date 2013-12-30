from rest_framework import permissions, viewsets
from core.permissions import IsOwnerOrReadOnly

from engagements.models import Engagement
from engagements.serializers import EngagementSerializer

class EngagementDetail(viewsets.ModelViewSet):
    queryset = Engagement.objects.all()
    serializer_class = EngagementSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, IsOwnerOrReadOnly)
