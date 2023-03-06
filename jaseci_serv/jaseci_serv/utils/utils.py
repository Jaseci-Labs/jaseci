try:
    from hmac import compare_digest
except ImportError:

    def compare_digest(a, b):
        return a == b


import binascii
from knox.crypto import hash_token
from knox.models import AuthToken
from knox.settings import CONSTANTS


def is_token_valid(token: str) -> bool:
    for auth_token in AuthToken.objects.filter(
        token_key=token[: CONSTANTS.TOKEN_KEY_LENGTH]
    ):
        try:
            digest = hash_token(token)
            return (
                compare_digest(digest, auth_token.digest) and auth_token.user.is_active
            )
        except (TypeError, binascii.Error):
            pass
    raise False
