from core.models import EventUpload
from core.serializers import EventUploadSerializer
from rest_framework import generics
from core.permissions import IsOwner

class EventUploadList(generics.ListAPIView):
    serializer_class = EventUploadSerializer
    permission_classes = (IsOwner,)

    def get_queryset(self):
        return EventUpload.objects.filter(user=self.request.user)
