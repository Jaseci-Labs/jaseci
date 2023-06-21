import base64

from django.contrib.auth import authenticate, get_user_model
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django_rest_passwordreset.signals import reset_password_token_created
from rest_framework import serializers

from jaseci.jsorc.jsorc import JsOrc
from jaseci_serv.svc.mail_svc import Mailer

requests_for_emails = None


def send_activation_email(email):
    """Construct activation email body"""
    code = base64.b64encode(email.encode()).decode()
    if requests_for_emails is not None:
        link = requests_for_emails.build_absolute_uri(
            reverse("user_api:activate", kwargs={"code": code})
        )
    else:
        link = "invalid"
    JsOrc.svc("mail").poke(Mailer).send_activation_email(email, code, link)


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):
    JsOrc.svc("mail").poke(Mailer).send_reset_email(
        reset_password_token.user.email, reset_password_token.key
    )


class UserSerializer(serializers.ModelSerializer):
    """Serializer for users object"""

    class Meta:
        model = get_user_model()
        fields = ("id", "email", "password", "name", "is_activated", "is_superuser")
        extra_kwargs = {"password": {"write_only": True, "min_length": 8}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        created_object = get_user_model().objects.create_user(**validated_data)
        if getattr(self, "_send_email", True) and not created_object.is_activated:
            send_activation_email(created_object.email)
        return created_object

    def update(self, instance, validated_data):
        """Update user, setting the password if needed"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class SuperUserSerializer(UserSerializer):
    """Serializer for users object"""

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_superuser(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""

    email = serializers.CharField()
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
        """
        Validate and authenticate the user
        """
        email = attrs.get("email").lower()
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"), username=email, password=password
        )
        if not user:
            msg = _("Unable to authenticate with provided credentials")
            raise serializers.ValidationError(msg, code="authorization")
        elif not user.is_activated:
            msg = _(
                "User not activated. Resending activation email.\n"
                + "Please check your email."
            )
            send_activation_email(email)
            raise serializers.ValidationError(msg)

        attrs["user"] = user
        return attrs
