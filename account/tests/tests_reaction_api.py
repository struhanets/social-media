from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from account.models import Profile, Reaction, Post
from account.serializers import ReactionListSerializer

REACTION_URL = reverse("account:reaction-list")


class ReactionUnAuthTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(REACTION_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ReactionAuthTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user1 = get_user_model().objects.create_user(
            email="test@example.com", password="default12345"
        )
        self.client.force_authenticate(user=self.user1)
        self.profile1 = Profile.objects.create(
            user=self.user1,
            first_name="test",
            last_name="test_last",
        )

        self.post1 = Post.objects.create(
            title="Simple Title",
            author=self.profile1,
            description="Default Text",
        )
        self.post2 = Post.objects.create(
            title="Simple Title 2",
            author=self.profile1,
            description="Default Text 2",
        )

    def test_reaction_list(self):
        reactions1 = Reaction.objects.create(
            user=self.profile1,
            post=self.post1,
            reaction_type=Reaction.ReactionChoices.LIKE,
        )
        reactions2 = Reaction.objects.create(
            user=self.profile1,
            post=self.post2,
            reaction_type=Reaction.ReactionChoices.DISLIKE,
        )

        response = self.client.get(REACTION_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        reactions = Reaction.objects.all()
        serializer = ReactionListSerializer(reactions, many=True)
        self.assertEqual(len(response.data["results"]), reactions.count())
        self.assertEqual(response.data["results"], serializer.data)

    def test_create_reaction(self):
        payload = {
            "user": self.profile1.id,
            "post": self.post1.id,
            "reaction_type": Reaction.ReactionChoices.LIKE,
        }

        response = self.client.post(REACTION_URL, payload)

        reaction = Reaction.objects.get(id=response.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for key in payload.keys():
            if key == "user":
                self.assertEqual(payload[key], self.user1.id)
            elif key == "post":
                self.assertEqual(payload[key], self.post1.id)
            else:
                self.assertEqual(payload[key], getattr(reaction, key))
