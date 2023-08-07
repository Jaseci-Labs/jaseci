import os
from uuid import uuid4
from json import loads, dumps

from asgiref.sync import async_to_sync
from channels.layers import settings
from channels.generic.websocket import WebsocketConsumer

from .event_action import authenticated_user
from jaseci_serv.base.models import lookup_global_config


class SocketConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        session_id = None
        authenticated = False
        target = self.scope["url_route"]["kwargs"]["target"]

        if target == "anonymous":
            self.target = session_id = str(uuid4())
        else:
            user = authenticated_user(target)
            if user:
                self.target = user.master.urn[9:]
                authenticated = True
            else:
                self.target = session_id = str(uuid4())

        async_to_sync(self.channel_layer.group_add)(self.target, self.channel_name)
        self.send(
            text_data=dumps(
                {
                    "type": "connect",
                    "authenticated": authenticated,
                    "session_id": session_id,
                }
            )
        )

    def receive(self, text_data=None, bytes_data=None):
        data = loads(text_data)

        async_to_sync(self.channel_layer.group_send)(
            self.target, {"type": "notify", "data": data}
        )

    def notify(self, data):
        self.send(text_data=dumps(data))


setattr(
    settings,
    "CHANNEL_LAYERS",
    {
        "default": loads(
            lookup_global_config(
                "CHANNEL_LAYER", '{"BACKEND": "channels.layers.InMemoryChannelLayer"}'
            )
        )
    },
)
