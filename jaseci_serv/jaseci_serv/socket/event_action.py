try:
    from hmac import compare_digest
except ImportError:

    def compare_digest(a, b):
        return a == b


import binascii
from knox.crypto import hash_token
from knox.models import AuthToken
from knox.settings import CONSTANTS
from jaseci.jsorc.live_actions import jaseci_action
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils import timezone


def authenticated_user(token: str):
    for auth_token in AuthToken.objects.filter(
        token_key=token[: CONSTANTS.TOKEN_KEY_LENGTH]
    ):
        try:
            digest = hash_token(token)
            if (
                compare_digest(digest, auth_token.digest)
                and auth_token.expiry > timezone.now()
            ):
                return auth_token.user
        except (TypeError, binascii.Error):
            pass
    return None


@jaseci_action(act_group=["ws"])
def notify_channel(target: str, data: dict):
    async_to_sync(get_channel_layer().send)(target, {"type": "notify", "data": data})


@jaseci_action(act_group=["ws"])
def notify_group(target: str, data: dict):
    async_to_sync(get_channel_layer().group_send)(
        target, {"type": "notify", "data": data}
    )
