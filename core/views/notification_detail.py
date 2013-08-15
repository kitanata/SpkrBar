from core.models import Notification
from core.serializers import NotificationSerializer
from rest_framework import generics, permissions, viewsets

class NotificationDetail(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
