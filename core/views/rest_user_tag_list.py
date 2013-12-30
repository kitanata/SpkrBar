from core.models import UserTag
from core.serializers import UserTagSerializer
from rest_framework import permissions, viewsets, generics
from core.permissions import IsOwnerOrReadOnly

class UserTagList(generics.ListAPIView):
    queryset = UserTag.objects.all()
    serializer_class = UserTagSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, IsOwnerOrReadOnly)
