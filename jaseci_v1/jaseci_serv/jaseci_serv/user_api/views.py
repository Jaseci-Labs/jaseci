from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework import renderers, status
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login, get_user_model
from django.contrib.auth.signals import user_logged_out
from knox.auth import TokenAuthentication

from jaseci_serv.user_api.serializers import UserSerializer
from jaseci_serv.user_api.serializers import SuperUserSerializer
from jaseci_serv.user_api.serializers import AuthTokenSerializer
from jaseci_serv.base.models import lookup_global_config
from datetime import timedelta

from rest_framework.response import Response
import base64

from jaseci.jsorc.jsorc import JsOrc
from jaseci.utils.utils import logger, ColCodes as Cc


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""

    serializer_class = UserSerializer


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
        user_agent = request.META.get("HTTP_USER_AGENT", "")
        log_str = f"Login request from {Cc.TG}{user}{Cc.EC} via {user_agent}"
        log_dict = {
            "api_name": "login",
            "caller_name": str(user),
            "request_user_agent": user_agent,
        }
        log_dict["extra_fields"] = list(log_dict.keys())
        logger.info(log_str, extra=log_dict)

        login(request, user)
        res = super(CreateTokenView, self).post(request, format=None)

        log_str = f"Login success for {Cc.TG}{user}{Cc.EC} via {user_agent}"
        log_dict = {
            "api_name": "login",
            "caller_name": str(user),
            "request_user_agent": user_agent,
        }
        log_dict["extra_fields"] = list(log_dict.keys())
        logger.info(log_str, extra=log_dict)
        return res


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""

    # TODO: re-activate when user changes email address or disable email change
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user

    def process_update(self, request, *args, **kwargs):
        user = request.user
        current_user = {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "is_activated": user.is_activated,
            "is_superuser": user.is_superuser,
        }

        response = self.update(request, *args, **kwargs)

        elastic = JsOrc.svc("elastic")
        if elastic.is_running():
            activity = elastic.app.generate_from_request(request)

            user = response.data

            activity["misc"] = {
                "old": current_user,
                "new": {
                    "id": user["id"],
                    "email": user["email"],
                    "name": user["name"],
                    "is_activated": user["is_activated"],
                    "is_superuser": user["is_superuser"],
                },
            }
            elastic.app.doc_activity(activity)

        return response

    def put(self, request, *args, **kwargs):
        return self.process_update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.process_update(request, *args, **kwargs)


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


class IsSuperUser(permissions.BasePermission):
    """
    Allows access only to super users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class UpdateUserView(APIView):
    """
    update specific user's is_activated and is_superuser
    """

    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsSuperUser)

    def update_field(self, user, data: dict, field_map: dict):
        has_changes = False
        for field, _type in field_map.items():
            if field in data and type(data[field]) is _type:
                if getattr(user, field, _type()) != data[field]:
                    setattr(user, field, data[field])
                    has_changes = True

        return has_changes

    def post(self, request, id):
        user = get_user_model().objects.get(id=id)

        current_user = {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "is_activated": user.is_activated,
            "is_superuser": user.is_superuser,
        }

        if user is None or not request.data or type(request.data) is not dict:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if self.update_field(
            user, request.data, {"is_activated": bool, "is_superuser": bool}
        ):
            user.save()

            elastic = JsOrc.svc("elastic")
            if elastic.is_running():
                activity = elastic.app.generate_from_request(request)

                activity["misc"] = {
                    "old": current_user,
                    "new": {
                        "id": user.id,
                        "email": user.email,
                        "name": user.name,
                        "is_activated": user.is_activated,
                        "is_superuser": user.is_superuser,
                    },
                }
                elastic.app.doc_activity(activity)

            return Response("Update Success!")
        else:
            return Response("No changes found!")
