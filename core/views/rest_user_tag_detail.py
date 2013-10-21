from core.models import UserTag
from core.serializers import UserTagSerializer
from rest_framework import generics, permissions, viewsets

class UserTagDetail(viewsets.ModelViewSet):
    queryset = UserTag.objects.all()
    serializer_class = UserTagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
