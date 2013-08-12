from talks.models import TalkLink
from talks.serializers import TalkLinkSerializer
from rest_framework import generics, permissions, viewsets

class TalkLinkList(generics.ListAPIView):
    serializer_class = TalkLinkSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return TalkLink.objects.filter(talk__pk=self.kwargs['talk_id'])
