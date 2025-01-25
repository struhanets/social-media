from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings
from drf_spectacular.utils import extend_schema

from user.serializers import UserSerializer, AuthTokenSerializer


@extend_schema(
    tags=["User"],
    description="Endpoint for user registration. "
    "Accepts email, password, and other optional "
    "fields to create a new user account.",
    request=UserSerializer,
    responses={201: UserSerializer, 400: "Validation errors"},
)
class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)


@extend_schema(
    tags=["Authentication"],
    description="Endpoint for user login. "
    "Accepts user credentials (email and password) "
    "and returns an authentication token for "
    "accessing protected resources.",
    request=AuthTokenSerializer,
    responses={
        200: {
            "type": "object",
            "properties": {
                "token": {
                    "type": "string",
                    "description": "Authentication token for the user",
                }
            },
        },
        400: "Invalid credentials or missing fields",
    },
)
class LoginUserView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = AuthTokenSerializer


@extend_schema(
    tags=["User Management"],
    description="Endpoint for retrieving and updating "
    "the current user's details. "
    "The user must be authenticated.",
)
class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
