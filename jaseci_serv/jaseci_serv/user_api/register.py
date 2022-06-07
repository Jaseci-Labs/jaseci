import os

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from rest_framework.exceptions import AuthenticationFailed
from knox.models import AuthToken

# def generate_username(name):

#     # username = "".join(name.split(' ')).lower()
#     if not User.objects.filter(username=username).exists():
#         return username
#     else:
#         random_username = username + str(random.randint(0, 1000))
#         return generate_username(random_username)


def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = get_user_model().objects.filter(email=email)
    if filtered_user_by_email.exists():

        if provider == filtered_user_by_email.first().auth_provider:

            registered_user = authenticate(
                email=email, password=settings.SOCIAL_SECRET)
            return {
                'email': registered_user.email,
                "message": "user logged in successfully "}

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' +
                filtered_user_by_email[0].auth_provider
            )

    else:
        user = {
            # 'username': generate_username(name),
            'email': email,
            'password': settings.SOCIAL_SECRET}
        user = get_user_model().objects.create_user(**user)
        user.is_verified = True
        user.auth_provider = provider
        user.is_staff = False
        user.is_admin = False
        user.save()
        tokens = AuthToken.objects.create(user)
        auth_user = authenticate(
            email=email, password=settings.SOCIAL_SECRET)
        return {
            'email': auth_user.email ,
            'tokens': tokens[1]
        }
