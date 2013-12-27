from core.models import SpkrbarUser
from core.serializers import UserSerializer

from rest_framework import permissions, viewsets, generics
from core.permissions import IsOwnerOrReadOnly

class UserDetail(viewsets.ModelViewSet):
    queryset = SpkrbarUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, IsOwnerOrReadOnly)
