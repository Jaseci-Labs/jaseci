from jaseci.utils.utils import logger
from jaseci.jsorc.jsorc import JsOrc
from jaseci.extens.svc.socket_svc import SocketService as Ss

try:
    from hmac import compare_digest
except ImportError:

    def compare_digest(a, b):
        return a == b


import binascii
from knox.crypto import hash_token
from knox.models import AuthToken
from knox.settings import CONSTANTS
from django.db import connection
from django.utils import timezone
from websocket import WebSocketApp as wsa

#################################################
#                 SOCKET APP ORM                 #
#################################################


@JsOrc.service(
    name="socket",
    config="SOCKET_CONFIG",
    manifest="SOCKET_MANIFEST",
    priority=1,
    pre_loaded=True,
)
class SocketService(Ss):
    def client_connect(self, ws: wsa, data: dict):
        user = "public"
        token = data.pop("token", None)
        data["authenticated"] = False

        if token:
            auth = self.authenticate(token)
            if auth:
                user = auth.master.urn[9:]
                data["authenticated"] = True

        data["user"] = user
        self.send(
            ws,
            {"type": "client_connected", "data": data},
        )

    def authenticate(self, token: str):
        try:
            connection.connect()
            for auth_token in AuthToken.objects.filter(
                token_key=token[: CONSTANTS.TOKEN_KEY_LENGTH]
            ):
                digest = hash_token(token)
                if compare_digest(digest, auth_token.digest) and (
                    not auth_token.expiry or auth_token.expiry > timezone.now()
                ):
                    return auth_token.user
        except Exception:
            logger.exception("Error authenticating socket!")
        return None
