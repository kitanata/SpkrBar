from talkevents.models import TalkEvent
from talkevents.serializers import EngagementSerializer
from rest_framework import generics, permissions

class EngagementList(generics.ListAPIView):
    queryset = TalkEvent.objects.all()
    serializer_class = EngagementSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
