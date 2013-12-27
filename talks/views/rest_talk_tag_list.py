from talks.models import TalkTag
from talks.serializers import TalkTagSerializer
from rest_framework import permissions, generics
from core.permissions import IsOwnerOrReadOnly

class TalkTagList(generics.ListAPIView):
    queryset = TalkTag.objects.all()
    serializer_class = TalkTagSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, IsOwnerOrReadOnly)
