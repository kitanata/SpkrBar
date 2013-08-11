from talks.models import Talk
from talks.serializers import TalkTagListSerializer
from rest_framework import generics, permissions, viewsets

class TalkTagList(generics.ListAPIView):
    queryset = Talk.objects.all()
    serializer_class = TalkTagListSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
