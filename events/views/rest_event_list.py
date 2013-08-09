from events.models import Event
from events.serializers import EventSerializer 
from rest_framework import generics, permissions

class EventList(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
