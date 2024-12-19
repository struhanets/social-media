from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from account.models import Profile
from account.serializers import ProfileListSerializer

PROFILE_URL_LIST = reverse("account:profile-list")


def detail_url(profile_id):
    return reverse("account:profile-detail", args=[profile_id])


class ProfileUnAuthTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(PROFILE_URL_LIST)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ProfileAuthTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user1 = get_user_model().objects.create_user(
            email="test@test.com", password="test12345"
        )
        self.user2 = get_user_model().objects.create_user(
            email="test2@test.com", password="testpassword"
        )

        self.client.force_authenticate(self.user1)

    def test_profiles_retrieve_access(self):
        profile = Profile.objects.create(
            user=self.user1,
            first_name="test",
            last_name="test_last",
        )
        response = self.client.get(detail_url(profile.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "test")
        self.assertEqual(response.data["last_name"], "test_last")

    def test_profiles_update(self):
        profile1 = Profile.objects.create(
            user=self.user1,
            first_name="test",
            last_name="test_last",
        )
        response = self.client.patch(detail_url(profile1.id), {"first_name": "test2"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "test2")

    def test_profiles_filter_by_last_name(self):
        profile1 = Profile.objects.create(
            user=self.user1,
            first_name="some",
            last_name="test_last",
        )
        response = self.client.get(
            PROFILE_URL_LIST, {"last_name": f"{profile1.last_name}"}
        )
        serializer = ProfileListSerializer([profile1], many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_profiles_filter_by_first_name(self):
        profile1 = Profile.objects.create(
            user=self.user1,
            first_name="test",
            last_name="test_last",
        )
        profile2 = Profile.objects.create(
            user=self.user2,
            first_name="first",
            last_name="last",
        )
        response = self.client.get(PROFILE_URL_LIST, {"first_name": "test"})
        serializer1 = ProfileListSerializer(profile1)
        serializer2 = ProfileListSerializer(profile2)
        self.assertIn(serializer1.data, response.data["results"])
        self.assertNotIn(serializer2.data, response.data["results"])

    def test_profile_create(self):
        user = self.user1
        payload = {
            "user": user.id,
            "first_name": "first_name_test",
            "last_name": "last_name_test",
        }

        response = self.client.post(PROFILE_URL_LIST, payload)

        profile = Profile.objects.get(id=response.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for key in payload.keys():
            if key == "user":
                self.assertEqual(payload[key], profile.user.id)
            else:
                self.assertEqual(payload[key], getattr(profile, key))
