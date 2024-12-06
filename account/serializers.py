from rest_framework import serializers

from account.models import Profile, Post, Reaction, Comment


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


class PostSerializer(serializers.ModelSerializer):
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


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = (
            "id",
            "user",
            "post",
            "reaction_type",
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "author",
            "description",
            "created_at",
        )
