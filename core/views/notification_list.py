from core.models import Notification
from core.serializers import NotificationSerializer
from rest_framework import permissions, viewsets, generics
from core.permissions import IsOwnerOrReadOnly

class NotificationList(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly, IsOwnerOrReadOnly)

    def get_queryset(self):
        return Notification.objects.filter(user__pk=self.kwargs['user_id'])
