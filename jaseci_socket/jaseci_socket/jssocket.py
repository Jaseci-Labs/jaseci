import sys
import http
import asyncio
import websockets
import logging
from os import environ
from redis import Redis

logging.basicConfig(
    format="%(asctime)s %(message)s",
    level=logging.INFO,
)


class LoggerAdapter(logging.LoggerAdapter):
    """Add connection ID and client IP address to websockets logs."""

    def process(self, msg, kwargs):
        try:
            websocket = kwargs["extra"]["websocket"]
        except KeyError:
            return msg, kwargs
        xff = websocket.request_headers.get("X-Forwarded-For")
        return f"{websocket.id} {xff} {msg}", kwargs


class JsSocket:
    _prefix = environ.get("REDIS_PREFIX", "jws-")
    _redis = Redis(
        host=environ.get("REDIS_HOST", "localhost"),
        port=int(environ.get("REDIS_PORT", "6379")),
        db=int(environ.get("REDIS_DB", "0")),
        decode_responses=True,
    )

    def __init__(self):
        self._redis.ping()
        self.method = {}

    async def consume(self, websocket):
        async for message in websocket:

            await websocket.send(message)

    async def health_check(self, path, request_headers):
        if path == "/healthz":
            return http.HTTPStatus.OK, [], b"OK\n"
        if path == "/terminate":
            loop = asyncio.get_running_loop()
            loop.call_later(1, sys.exit, 69)
            return http.HTTPStatus.OK, [], b"Terminating\n"

    def serve(self, *args, **kwargs):
        return websockets.serve(
            self.consume,
            *args,
            process_request=self.health_check,
            logger=LoggerAdapter(logging.getLogger("websockets.server"), None),
            **kwargs,
        )
