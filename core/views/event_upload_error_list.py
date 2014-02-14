from core.models import EventUploadError
from core.serializers import EventUploadErrorSerializer
from rest_framework import generics
from core.permissions import IsOwner

class EventUploadErrorList(generics.ListAPIView):
    serializer_class = EventUploadErrorSerializer
    permission_classes = (IsOwner,)

    def get_queryset(self):
        return EventUploadError.objects.filter(event_upload__pk=self.kwargs['pk'])