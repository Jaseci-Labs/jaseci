from rest_framework import generics, authentication, permissions
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework import renderers

from user_api.serializers import UserSerializer
from user_api.serializers import AuthTokenSerializer
from user_api.serializers import send_activation_email

from django.contrib.auth import get_user_model
from rest_framework.response import Response
import base64


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """Perform create override to send out activation Email"""
        created_object = serializer.save()
        send_activation_email(self.request, created_object.email)


class ActivateUserView(APIView):
    """Create a new user in the system"""
    # TODO: Add Test case
    renderer_classes = [renderers.JSONRenderer]

    def get(self, request, code):
        """Perform create override to send out activation Email"""
        email = base64.b64decode(code).decode()
        user = get_user_model().objects.get(email=email)
        if (not user):
            return Response('Invalid activation code/link!')
        user.is_activated = True
        user.save()
        return Response('User successfully activated!')


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    # TODO: re-activate when user changes email address or disable email change
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user
