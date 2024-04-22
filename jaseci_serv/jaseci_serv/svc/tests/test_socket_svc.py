from jaseci.utils.utils import TestCaseHelper
from jaseci.jsorc.jsorc import JsOrc
from jaseci_serv.svc.socket_svc import SocketService

from orjson import dumps
from json import loads
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from websocket import create_connection
from websocket import WebSocket


def override_authenticate(self, token: str):
    try:
        # removing reconnection since unit test use on memory db
        return self.authenticator.authenticate_credentials(token.encode())[0]
    except Exception:
        return None


class SocketServiceTest(TestCaseHelper, TestCase):
    def setUp(self):
        super().setUp()
        self.admin = get_user_model().objects.create_superuser(
            "admin@jaseci.com", "password"
        )

        # since pytest uses in memory database we need to
        # get the token first before opening socket service
        self.token = (
            APIClient()
            .post(
                reverse("user_api:token"),
                {"email": "admin@jaseci.com", "password": "password"},
            )
            .data["token"]
        )

        JsOrc.settings("SOCKET_CONFIG").update(
            {
                "enabled": True,
                "url": "ws://localhost:8002/ws",
                "ping_url": "http://localhost:8002/healthz",
            }
        )
        JsOrc._services["socket"][0]["type"].authenticate = override_authenticate

    def socket_process(self, ws: WebSocket, token: str = None):
        data = {}
        if token:
            data["token"] = token

        ws.send(dumps({"type": "client_connect", "data": data}))
        event: dict = loads(ws.recv())

        self.assertEqual("client_connected", event.get("type"))
        data: dict = event.get("data")
        target = data.get("target")
        self.assertTrue(data)
        self.assertTrue(target)
        self.assertTrue(data.get("authenticated") == bool(token))

        ws.send(
            dumps(
                {
                    "type": "notify_client",
                    "data": {"target": target, "data": {"test": 1}},
                }
            )
        )
        event: dict = loads(ws.recv())
        self.assertEqual({"test": 1}, event)

        ws.send(
            dumps(
                {
                    "type": "notify_group",
                    "data": {"target": target, "data": {"test": 2}},
                }
            )
        )
        event: dict = loads(ws.recv())
        self.assertEqual({"test": 2}, event)

    @JsOrc.inject(services=["socket"])
    def test_socket(self, socket: SocketService):
        self.assertTrue(socket.is_running())

        ws = create_connection("ws://localhost:8002/ws")

        self.socket_process(ws)
        self.socket_process(ws, self.token)

        ws.close()
