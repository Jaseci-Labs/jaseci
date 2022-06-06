from django.contrib.auth import authenticate
import os
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from django.conf import settings


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

        if provider == filtered_user_by_email[0].auth_provider:

            registered_user = authenticate(
                email=email, password=settings.SOCIAL_SECRET)

            return {
                # 'username': registered_user.username,
                'email': registered_user.email,
                'tokens': registered_user.tokens()}

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' +
                filtered_user_by_email[0].auth_provider
            )

    else:
        user = {
            # 'username': generate_username(name),
            'email': email,
            'password': os.environ.get('SOCIAL_SECRET')}
        user = get_user_model.objects.create_user(**user)
        user.is_verified = True
        user.auth_provider = provider
        user.save()

        new_user = authenticate(
            email=email, password=os.environ.get('SOCIAL_SECRET'))
        return {
            'email': new_user.email,
            # 'username': new_user.username,
            'tokens': new_user.tokens()
        }
