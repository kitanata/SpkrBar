from talks.models import Talk
from talks.serializers import TalkSerializer
from rest_framework import generics, permissions, viewsets

class TalkDetail(viewsets.ModelViewSet):
    queryset = Talk.objects.all()
    serializer_class = TalkSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
