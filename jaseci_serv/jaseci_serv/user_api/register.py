from django.contrib.auth import authenticate, get_user_model
from django.forms import DateTimeField
from rest_framework.exceptions import AuthenticationFailed
from knox.models import AuthToken
from jaseci_serv.base.socialauth import socialauth_config
from knox.settings import knox_settings
import hashlib, uuid


# def generate_username(name):

#     # username = "".join(name.split(' ')).lower()
#     if not User.objects.filter(username=username).exists():
#         return username
#     else:
#         random_username = username + str(random.randint(0, 1000))
#         return generate_username(random_username)


def get_hashed_password(email=""):
    social_auth = socialauth_config()
    email = email
    salt = social_auth.get_social_secret()
    hashed_password = hashlib.sha256((email + salt).encode("utf-8")).hexdigest()
    return hashed_password


def register_social_user(request, provider, user_id, email, name):
    filtered_user_by_email = get_user_model().objects.filter(email=email)

    if filtered_user_by_email.exists():

        if provider == filtered_user_by_email.first().auth_provider:

            registered_user = authenticate(
                equest=request, username=email, password=get_hashed_password(email)
            )
            instanse, token = AuthToken.objects.create(registered_user)
            return {
                "email": registered_user.email,
                "token": token,
                "exp": instanse.expiry,
                "user": registered_user,
            }

        else:
            raise AuthenticationFailed(
                detail="Please continue your login using "
                + filtered_user_by_email[0].auth_provider
            )

    else:
        user = {"email": email, "password": get_hashed_password(email)}
        user = get_user_model().objects.create_user(**user)
        user.name = name
        user.is_verified = True
        user.auth_provider = provider
        user.is_staff = False
        user.is_admin = False
        user.save()
        instanse, token = AuthToken.objects.create(user)
        auth_user = authenticate(
            request=request, username=email, password=get_hashed_password(email)
        )
        # user = authenticate(username=username, password=password)
        return {
            "email": auth_user.email,
            "token": token,
            "user": auth_user,
            "exp": instanse.expiry,
        }
