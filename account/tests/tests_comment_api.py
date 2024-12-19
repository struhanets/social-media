from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from account.models import Profile, Comment, Post
from account.serializers import CommentSerializer

COMMENT_URL = reverse("account:comment-list")


def detail_url(comment_id):
    return reverse("account:comment-detail", args=[comment_id])


class CommentUnAuthTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(COMMENT_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CommentAuthTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user1 = get_user_model().objects.create_user(
            email="test@example.com", password="default12345"
        )
        self.user2 = get_user_model().objects.create_user(
            email="test2@test.com", password="testpassword"
        )
        self.client.force_authenticate(user=self.user1)
        self.profile = Profile.objects.create(
            user=self.user1,
            first_name="test",
            last_name="test_last",
        )
        self.post = Post.objects.create(
            title="test post", author=self.profile, description="test description"
        )

    def test_comment_list(self):
        comment = Comment.objects.create(
            author=self.profile,
            post=self.post,
        )

        response = self.client.get(COMMENT_URL)

        comments = Comment.objects.all()

        serializer = CommentSerializer(comments, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), comments.count())
        self.assertEqual(response.data["results"], serializer.data)

    def test_comment_update(self):
        comment = Comment.objects.create(
            author=self.profile, post=self.post, description="test description"
        )

        response = self.client.patch(
            detail_url(comment.id), {"description": "another text"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["description"], "another text")

    def test_comment_create(self):
        profile2 = Profile.objects.create(
            user=self.user2,
            first_name="second",
            last_name="second_last",
        )

        payload = {
            "author": profile2.id,
            "post": self.post.id,
            "description": "some text description",
        }

        response = self.client.post(COMMENT_URL, payload)

        comment = Comment.objects.get(id=response.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for key in payload.keys():
            if key == "author":
                self.assertEqual(payload[key], comment.author.id)
            elif key == "post":
                self.assertEqual(payload[key], comment.post.id)
            else:
                self.assertEqual(payload[key], getattr(comment, key))
