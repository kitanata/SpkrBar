from talks.models import TalkSlideDeck
from talks.serializers import TalkSlideDeckSerializer
from rest_framework import generics, permissions, viewsets

class TalkSlideDeckDetail(viewsets.ModelViewSet):
    queryset = TalkSlideDeck.objects.all()
    serializer_class = TalkSlideDeckSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
