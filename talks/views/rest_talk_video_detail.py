from talks.models import TalkVideo
from talks.serializers import TalkVideoSerializer
from rest_framework import generics, permissions, viewsets

class TalkVideoDetail(viewsets.ModelViewSet):
    queryset = TalkVideo.objects.all()
    serializer_class = TalkVideoSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
