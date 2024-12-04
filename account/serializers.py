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
