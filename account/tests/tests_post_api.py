from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from account.models import Profile, Post
from account.serializers import PostSerializer, PostListSerializer

POST_URL = reverse("account:post-list")


def detail_url(post_id):
    return reverse("account:post-detail", args=[post_id])


class PostUnAuthTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(POST_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PostAuthTests(TestCase):
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

    def test_post_list(self):
        post = {
            "title": "Sample Title",
            "author": self.profile,
            "description": "Sample Description",
        }
        response = self.client.get(POST_URL)

        posts = Post.objects.all()
        serializer = PostListSerializer(posts, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_post_following_list(self):
        following_profile = Profile.objects.create(
            user=self.user2,
            first_name="following_first",
            last_name="following_last",
        )

        following_post = Post.objects.create(
            title="Sample Title",
            author=self.profile,
            description="Sample Description",
        )
        response = self.client.get(POST_URL)

        posts = Post.objects.all()
        serializer = PostListSerializer(posts, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_post_detail_access(self):
        post = Post.objects.create(
            title="Sample Title",
            author=self.profile,
            description="Sample Description",
        )

        response = self.client.get(detail_url(post.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Sample Title")
        self.assertEqual(response.data["description"], "Sample Description")

    def test_post_update(self):
        post = Post.objects.create(
            title="Sample Title",
            author=self.profile,
            description="Sample Description",
        )

        response = self.client.patch(detail_url(post.id), {"title": "Updated"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated")

    def test_filter_by_tag(self):
        post1 = Post.objects.create(
            title="Sample Title 3",
            author=self.profile,
            description="Sample Description",
        )
        post1.tags.add("tag1", "tag2")
        post2 = Post.objects.create(
            title="Sample Title2",
            author=self.profile,
            description="Another Sample Description",
        )
        post2.tags.add("test1", "test2")

        response = self.client.get(POST_URL, {"tags": "tag1"})

        serializer1 = PostListSerializer(post1)
        serializer2 = PostListSerializer(post2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(serializer2.data, response.data["results"])
        self.assertIn(serializer1.data, response.data["results"])

    def test_create_post(self):
        profile = Profile.objects.get(
            user=self.user1,
        )

        payload = {
            "title": "Sample Title",
            "author": profile.id,
            "description": "Default Text",
            "tags": ["tag1", "tag2"],
        }
        response = self.client.post(POST_URL, payload)

        post = Post.objects.get(id=response.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for key in payload.keys():
            if key == "author":
                self.assertEqual(payload[key], post.author.id)
            elif key == "tags":
                self.assertEqual(set(payload[key]), set(post.tags.names()))
            else:
                self.assertEqual(payload[key], getattr(post, key))
