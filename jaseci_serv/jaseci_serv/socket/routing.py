from django.urls import path
from . import consumer

websocket_urlpatterns = [
    path(r"ws/socket-server/<str:target>", consumer.SocketConsumer.as_asgi())
]
