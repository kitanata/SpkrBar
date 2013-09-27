from locations.models import Location
from locations.serializers import LocationSerializer
from rest_framework import generics, permissions, viewsets

class LocationDetail(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
