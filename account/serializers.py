from rest_framework import serializers

from account.models import Profile, Post, Reaction, Comment
from taggit.serializers import TagListSerializerField, TaggitSerializer


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "first_name",
            "last_name",
            "image",
            "bio",
            "following",
        )


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("id", "first_name", "last_name")


class ProfileListSerializer(ProfileSerializer):
    following = FollowerSerializer(many=True, read_only=True)
    followers = FollowerSerializer(many=True, read_only=True)
    user = serializers.SlugRelatedField(read_only=True, slug_field="email")

    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "first_name",
            "last_name",
            "image",
            "bio",
            "following",
            "followers",
        )
        read_only_fields = ("id", "user", "image", "following", "followers")


class ProfileRetrieveSerializer(ProfileSerializer):
    following = FollowerSerializer(many=True, read_only=False)
    followers = FollowerSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = (
            "first_name",
            "last_name",
            "image",
            "bio",
            "following",
            "followers",
        )
        read_only_fields = ("id", "user", "followers")


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = (
            "id",
            "user",
            "post",
            "reaction_type",
        )


class ReactionListSerializer(ReactionSerializer):
    user = serializers.SlugRelatedField(slug_field="last_name", read_only=True)
    post = serializers.SlugRelatedField(slug_field="title", read_only=True)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "author",
            "post",
            "description",
            "created_at",
        )
        read_only_fields = ("id", "created_at")


class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "author",
            "description",
            "image",
            "pub_date",
            "tags",
            "comments",
        )
        read_only_fields = (
            "id",
            "pub_date",
            "comments",
        )


class PostListSerializer(PostSerializer):
    author = serializers.SlugRelatedField(slug_field="first_name", read_only=True)


class PostRetrieveSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "author",
            "description",
            "image",
            "comments",
            "pub_date",
        )
        read_only_fields = (
            "id",
            "author",
            "comments",
            "pub_date",
        )


class PostTitleSerializer(PostSerializer):
    class Meta:
        model = Post
        fields = ("id", "title")
