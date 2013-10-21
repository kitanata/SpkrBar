from core.models import UserLink
from core.serializers import UserLinkSerializer
from rest_framework import generics, permissions, viewsets

class UserLinkDetail(viewsets.ModelViewSet):
    queryset = UserLink.objects.all()
    serializer_class = UserLinkSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
