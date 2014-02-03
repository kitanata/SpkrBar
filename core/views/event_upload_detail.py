from core.models import EventUpload
from core.serializers import EventUploadSerializer
from rest_framework import viewsets
from core.permissions import IsOwner

class EventUploadDetail(viewsets.ModelViewSet):
    queryset = EventUpload.objects.all()
    serializer_class = EventUploadSerializer
    permission_classes = (IsOwner, )
