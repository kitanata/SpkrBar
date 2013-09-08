from engagements.models import Engagement
from engagements.serializers import EngagementSerializer
from rest_framework import generics, permissions

class EngagementList(generics.ListAPIView):
    serializer_class = EngagementSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return Engagement.objects.filter(confirmed=True)
