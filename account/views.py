from rest_framework import viewsets

from account.models import Profile, Post, Comment
from account.permissions import IsOwnerOrReadOnly
from account.serializers import (
    ProfileSerializer,
    PostSerializer,
    CommentSerializer,
    ProfileListSerializer,
    ProfileRetrieveSerializer,
)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileListSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return ProfileListSerializer
        elif self.action == "retrieve":
            return ProfileRetrieveSerializer

        return ProfileSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
