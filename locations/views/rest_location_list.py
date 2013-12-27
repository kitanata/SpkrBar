from locations.models import Location
from locations.serializers import LocationSerializer
from rest_framework import permissions, generics

class LocationList(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = (permissions.DjangoModelPermissionsOrAnonReadOnly,)
