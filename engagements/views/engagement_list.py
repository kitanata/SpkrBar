from engagements.models import Engagement
from engagements.serializers import EngagementSerializer
from rest_framework import permissions, viewsets, generics
from core.permissions import IsOwnerOrReadOnly

class EngagementList(generics.ListAPIView):
    serializer_class = EngagementSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, IsOwnerOrReadOnly)

    def get_queryset(self):
        return Engagement.objects.filter(confirmed=True)
