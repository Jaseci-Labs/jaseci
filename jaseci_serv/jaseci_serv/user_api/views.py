import base64
from datetime import timedelta

from django.contrib.auth import get_user_model, login
from django.contrib.auth.signals import user_logged_out
from knox.auth import TokenAuthentication
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions, renderers, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from jaseci_serv.base.models import lookup_global_config
from jaseci_serv.user_api.serializers import (
    AuthTokenSerializer,
    FacebookSocialAuthSerializer,
    GoogleSocialAuthSerializer,
    SuperUserSerializer,
    UserSerializer,
    send_activation_email,
)
from jaseci_serv.base.socialauth import socialauth_config


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""

    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """Perform create override to send out activation Email"""
        created_object = serializer.save()
        if not created_object.is_activated:
            send_activation_email(self.request, created_object.email)


class CreateSuperUserView(generics.CreateAPIView):
    """Create a new user in the system"""

    serializer_class = SuperUserSerializer


class ActivateUserView(APIView):
    """Create a new user in the system"""

    # TODO: Add Test case
    renderer_classes = [renderers.JSONRenderer]

    def get(self, request, code):
        """Perform create override to send out activation Email"""
        email = base64.b64decode(code).decode()
        user = get_user_model().objects.get(email=email)
        if not user:
            return Response("Invalid activation code/link!")
        user.is_activated = True
        user.save()
        return Response("User successfully activated!")


class CreateTokenView(KnoxLoginView):
    """Create a new auth token for user"""

    permission_classes = (permissions.AllowAny,)

    def get_token_ttl(self):
        ttl = lookup_global_config("LOGIN_TOKEN_TTL_HOURS", None)
        if not ttl:
            return super(CreateTokenView, self).get_token_ttl()
        else:
            return timedelta(hours=int(ttl))

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return super(CreateTokenView, self).post(request, format=None)


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""

    # TODO: re-activate when user changes email address or disable email change
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class LogoutAllUsersView(APIView):
    """
    Log out of all user sessions across all users
    I.E. deletes all auth tokens for all users
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

    def post(self, request, format=None):
        users = get_user_model().objects.all()
        for u in users:
            u.auth_token_set.all().delete()
            user_logged_out.send(sender=u.__class__, request=request, user=u)
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class GoogleSSOView(GenericAPIView):
    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        """
        POST with "auth_token"
        send an "id_token" from google
        """
        data = self.serializer_class(data=request.data, context={"request": request})
        if data.is_valid(raise_exception=True):
            auth_token = data.validated_data.get("auth_token")
            if auth_token["user"] is not None:
                login(
                    request,
                    auth_token["user"],
                    backend="django.contrib.auth.backends.ModelBackend",
                )
            return Response(
                {"token": auth_token["token"], "exp": auth_token["exp"]},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)


class GoogleSSOScriptView(GenericAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # TODO: make views to directly generate HTMl code snippet
        # for user which they can paste into their html page
        return Response({"sucess": True}, status=status.HTTP_200_OK)


class FacebookSSOView(GenericAPIView):
    serializer_class = FacebookSocialAuthSerializer

    def post(self, request):
        """
        POST with "auth_token"
        send an "id_token" from google
        """
        data = self.serializer_class(data=request.data)
        if data.is_valid(raise_exception=True):
            auth_token = data.validated_data.get("auth_token")
            return Response(auth_token, status=status.HTTP_200_OK)
        else:
            return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
