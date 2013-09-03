from core.models import Comment
from core.serializers import CommentSerializer
from rest_framework import generics, permissions, viewsets

class CommentDetail(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
