from talkevents.models import TalkEvent
from talkevents.serializers import EngagementSerializer
from rest_framework import generics, permissions

class EngagementList(generics.ListAPIView):
    serializer_class = EngagementSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return TalkEvent.objects.filter(confirmed=True)
