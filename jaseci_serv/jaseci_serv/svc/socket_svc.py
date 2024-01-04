from jaseci.utils.utils import logger
from jaseci.jsorc.jsorc import JsOrc
from jaseci.jsorc.jsorc_utils import ManifestType
from jaseci.extens.svc.socket_svc import SocketService as Ss

from django.db import connection
from knox.auth import TokenAuthentication
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
    def __init__(
        self,
        config: dict,
        manifest: dict,
        manifest_type: ManifestType = ManifestType.DEDICATED,
        source: dict = {},
    ):
        self.authenticator = TokenAuthentication()
        super().__init__(config, manifest, manifest_type, source)

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
            return self.authenticator.authenticate_credentials(token.encode())[0]
        except Exception:
            logger.exception("Error authenticating socket!")
        return None
