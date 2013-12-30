from core.models import UserLink
from core.serializers import UserLinkSerializer
from rest_framework import permissions, viewsets, generics
from core.permissions import IsOwnerOrReadOnly

class UserLinkDetail(viewsets.ModelViewSet):
    queryset = UserLink.objects.all()
    serializer_class = UserLinkSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, IsOwnerOrReadOnly)
