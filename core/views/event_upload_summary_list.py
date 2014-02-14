from core.models import EventUploadSummary
from core.serializers import EventUploadSummarySerializer
from rest_framework import generics
from core.permissions import IsOwner

class EventUploadSummaryList(generics.ListAPIView):
    serializer_class = EventUploadSummarySerializer
    permission_classes = (IsOwner,)

    def get_queryset(self):
        return EventUploadSummary.objects.filter(event_upload__pk=self.kwargs['pk'])