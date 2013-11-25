from core.models import UserTag
from core.serializers import UserTagSerializer
from rest_framework import generics, permissions, viewsets

class UserTagList(generics.ListAPIView):
    queryset = UserTag.objects.all()
    serializer_class = UserTagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
