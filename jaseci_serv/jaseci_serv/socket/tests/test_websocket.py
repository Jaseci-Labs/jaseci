import pytest
from uuid import UUID
from json import loads
from jaseci.utils.utils import TestCaseHelper
from django.test import TestCase

from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator


class WebSocketTests(TestCaseHelper, TestCase):
    """Test the publicly available node API"""

    def setUp(self):
        super().setUp()

        from ..routing import websocket_urlpatterns

        self.app = URLRouter(websocket_urlpatterns)

    def tearDown(self):
        super().tearDown()

    def is_valid_uuid(self, uuid):
        try:
            _uuid = UUID(uuid, version=4)
        except ValueError:
            return False
        return str(_uuid) == uuid

    @pytest.mark.asyncio
    async def test_websocket(self):
        communicator = WebsocketCommunicator(self.app, "ws/socket-server/anonymous")

        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)
        response: dict = loads(await communicator.receive_from())
        self.assertTrue(self.is_valid_uuid(response.pop("group")))
        self.assertTrue(response.pop("channel").startswith("specific."))
        self.assertEqual(response, {"type": "connect", "authenticated": False})

        await communicator.send_to(text_data='{"test": true}')
        response: dict = loads(await communicator.receive_from())
        self.assertEqual(response, {"type": "notify", "data": {"test": True}})

        await communicator.disconnect()
