from rest_framework import generics, permissions, viewsets

from engagements.models import Engagement
from engagements.serializers import EngagementSerializer

class EngagementDetail(viewsets.ModelViewSet):
    queryset = Engagement.objects.all()
    serializer_class = EngagementSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
