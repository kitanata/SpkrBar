from core.models import UserFollowing
from core.serializers import UserFollowingSerializer
from rest_framework import permissions, viewsets, generics
from core.permissions import IsOwnerOrReadOnly

class UserFollowingDetail(viewsets.ModelViewSet):
    queryset = UserFollowing.objects.all()
    serializer_class = UserFollowingSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, IsOwnerOrReadOnly)
