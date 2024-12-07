import os
import uuid

from django.db import models
from django.utils.text import slugify

from social_media_api.settings import AUTH_USER_MODEL
from taggit.managers import TaggableManager


def image_custom_path(instance, filename):
    _, extension = os.path.splitext(filename)

    if isinstance(instance, Profile):
        folder = "profile"
        return os.path.join(
            "upload",
            folder,
            "images",
            f"{slugify(instance.last_name)}-{uuid.uuid4()}{extension}",
        )
    if isinstance(instance, Post):
        folder = "post"
        return os.path.join(
            "upload",
            folder,
            "images",
            f"{slugify(instance.title)}-{uuid.uuid4()}{extension}",
        )


class Profile(models.Model):
    user = models.OneToOneField(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to=image_custom_path, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    following = models.ManyToManyField("Profile", related_name="followers", blank=True)

    class Meta:
        ordering = ("last_name",)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="posts")
    description = models.TextField()
    image = models.ImageField(upload_to=image_custom_path, blank=True, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()
    comments = models.ManyToManyField("Comment", related_name="posts", blank=True)

    class Meta:
        ordering = ("-pub_date",)

    def __str__(self):
        return f"{self.title} by {self.author}"


class Reaction(models.Model):
    class ReactionChoices(models.TextChoices):
        LIKE = "Like"
        DISLIKE = "Dislike"

    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=10, choices=ReactionChoices)

    class Meta:
        unique_together = (
            "user",
            "post",
        )


class Comment(models.Model):
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="comments"
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("author",)

    def __str__(self):
        return f"{self.author}"
