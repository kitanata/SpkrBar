from core.models import EventUpload
from core.serializers import EventUploadSerializer
from rest_framework import generics
from core.permissions import IsOwner

class EventUploadList(generics.ListAPIView):
    queryset = EventUpload.objects.all()
    serializer_class = EventUploadSerializer
    permission_classes = (IsOwner,)
