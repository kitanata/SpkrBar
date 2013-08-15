from core.models import Notification
from core.serializers import NotificationSerializer
from rest_framework import generics, permissions

class NotificationList(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        return Notification.objects.filter(dismissed=False, user__pk=self.kwargs['user_id'])
