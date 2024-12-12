from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from account.models import Profile, Post, Comment, Reaction
from account.permissions import IsOwnerOrReadOnly
from account.serializers import (
    ProfileSerializer,
    PostSerializer,
    CommentSerializer,
    ProfileListSerializer,
    ProfileRetrieveSerializer,
    PostRetrieveSerializer,
    ReactionSerializer,
    ReactionListSerializer,
    PostListSerializer,
    CommentCreateSerializer,
)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileListSerializer
    authentication_classes = (TokenAuthentication,)
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


class ReactionViewSet(viewsets.ModelViewSet):
    serializer_class = ReactionSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        return Reaction.objects.filter(user=self.request.user.profile)

    def create(self, request, *args, **kwargs):
        # Отримуємо користувача та пост
        user = request.user.profile
        post_id = request.data.get("post")
        reaction_type = request.data.get("reaction_type")

        if not post_id or not reaction_type:
            return Response(
                {"error": "Must be post and reaction_type"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Перевіряємо, чи вже існує реакція
        reaction, created = Reaction.objects.update_or_create(
            user=user,
            post_id=post_id,
            defaults={"reaction_type": reaction_type},
        )

        serializer = self.get_serializer(reaction)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

    def get_serializer_class(self):
        if self.action == "list":
            return ReactionListSerializer

        return ReactionSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)
    authentication_classes = (TokenAuthentication,)

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        if self.action == "retrieve":
            return PostRetrieveSerializer

        return PostSerializer

    def get_queryset(self):
        queryset = self.queryset
        profile = self.request.user.profile
        following = profile.following.all()
        if self.action == "list":
            queryset = queryset.filter(
                Q(author=profile) | Q(author__in=following)
            ).prefetch_related("author__user__profile", "comments")

            hash_tags = self.request.query_params.get("tags")
            if hash_tags:
                return queryset.filter(tags__name__icontains=hash_tags)

        return queryset

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.author != request.user.profile:
            return Response(
                {"detail": "You don't have permission to update this post"},
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().update(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = (TokenAuthentication,)

    def get_serializer_class(self):
        if self.action == "create":
            return CommentCreateSerializer

        return CommentSerializer
