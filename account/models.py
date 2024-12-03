from django.db import models

from social_media_api.settings import AUTH_USER_MODEL
from taggit.managers import TaggableManager


class Profile(models.Model):
    user = models.OneToOneField(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    following = models.ManyToManyField("Profile", related_name="followers", blank=True)


class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="posts")
    description = models.TextField()
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()
    comments = models.ManyToManyField("Comment", related_name="posts", blank=True)


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
