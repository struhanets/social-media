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

    def get_queryset(self):
        queryset = self.queryset

        last_name = self.request.query_params.get("last_name")
        first_name = self.request.query_params.get("first_name")
        if last_name:
            return queryset.filter(last_name__icontains=last_name)
        elif first_name:
            return queryset.filter(first_name__icontains=first_name)

        if self.action == "list":
            queryset = queryset.select_related()

        return queryset


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
