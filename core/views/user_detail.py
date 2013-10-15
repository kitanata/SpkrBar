from core.models import SpkrbarUser
from core.serializers import UserSerializer
from rest_framework import generics, permissions, viewsets

class UserDetail(generics.RetrieveUpdateAPIView):
    queryset = SpkrbarUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
