from talks.models import TalkLink
from talks.serializers import TalkLinkSerializer
from rest_framework import permissions, generics
from core.permissions import IsOwnerOrReadOnly

class TalkLinkList(generics.ListAPIView):
    serializer_class = TalkLinkSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, IsOwnerOrReadOnly)

    def get_queryset(self):
        return TalkLink.objects.filter(talk__pk=self.kwargs['talk_id'])
