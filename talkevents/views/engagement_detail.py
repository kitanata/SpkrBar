from talkevents.models import TalkEvent
from talkevents.serializers import EngagementSerializer
from rest_framework import generics, permissions

class EngagementDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TalkEvent.objects.all()
    serializer_class = EngagementSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
