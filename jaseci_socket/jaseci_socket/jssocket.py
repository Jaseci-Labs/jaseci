import sys
import http
import asyncio
import websockets
import logging
import bcrypt
from os import environ
from redis import Redis
from orjson import loads, dumps
from json import dumps as jdumps
from websockets.legacy.server import WebSocketServerProtocol as wssp
from websockets.exceptions import ConnectionClosed

logging.basicConfig(
    format="%(asctime)s %(message)s",
    level=logging.INFO,
)

EVENT_THRESHOLD = int(environ.get("EVENT_THRESHOLD", "50"))
EVENT_COUNT = 0


class LoggerAdapter(logging.LoggerAdapter):
    """Add connection ID and client IP address to websockets logs."""

    def process(self, msg, kwargs):
        xff = ""
        try:
            websocket = kwargs["extra"]["websocket"]
            xff = websocket.request_headers.get("X-Forwarded-For")
        except KeyError:
            return msg, kwargs

        return f"{websocket.id} {xff} {msg}", kwargs


class JsSocket:
    # _prefix = environ.get("REDIS_PREFIX", "jws-")
    # _redis = Redis(
    #     host=environ.get("REDIS_HOST", "localhost"),
    #     port=int(environ.get("REDIS_PORT", "6379")),
    #     db=int(environ.get("REDIS_DB", "0")),
    #     decode_responses=True,
    # )
    # _redis.ping()

    _servers = dict[str, wssp]()
    _clients = dict[str, wssp]()
    _groups = dict[str, set]()

    _servers_queue = list()

    def __init__(self, auth: str):
        self.auth = bytes.fromhex(auth)
        self.method = {
            "server_connect": self.server_connect,
            "client_connect": self.client_connect,
            "client_connected": self.client_connected,
            "client_disconnect": self.client_disconnect,
            "notify_client": self.notify_client,
            "notify_group": self.notify_group,
            "notify_all": self.notify_all,
        }

    async def cleanup(self):
        global EVENT_COUNT, EVENT_THRESHOLD
        EVENT_COUNT += 1
        if EVENT_COUNT % EVENT_THRESHOLD == 0:
            for group, members in self._groups.copy().items():
                if members:
                    for mem in members.copy():
                        if not self._clients.get(mem):
                            members.remove(mem)

                if not members:
                    self._groups.pop(group, None)
            await self.check_connection(self._clients)
            await self.check_connection(self._servers)

    async def check_connection(self, clients: dict[str, wssp]):
        for client in clients.copy().values():
            try:
                ping = await client.ping()
                await ping
            except ConnectionClosed:
                await self.closed(client)

    async def add_server(self, ws: wssp):
        ws_id = str(ws.id)
        self._servers[ws_id] = ws
        self._servers_queue.append(ws_id)

    async def client_send(self, ws: wssp, data: dict):
        try:
            await ws.send(jdumps(data))
        except ConnectionClosed:
            await self.closed(ws)

    async def server_send(self, data: dict):
        server_count = len(self._servers)
        if server_count > 1 and self._servers_queue:
            ws: wssp = None
            queue = self._servers_queue.pop(0)
            try:
                ws = self._servers.get(queue)
                if ws:
                    await ws.send(dumps(data))
                    self._servers_queue.append(queue)
            except ConnectionClosed:
                await self.closed(ws)
        elif server_count == 1:
            try:
                for ws in self._servers.values():
                    await ws.send(dumps(data))
            except ConnectionClosed:
                await self.closed(ws)

    async def server_connect(self, ws: wssp, data: dict):
        if bcrypt.checkpw(data.get("auth").encode("utf-8"), self.auth):
            await self.add_server(ws)
            await self.client_send(ws, {"type": "server_connect", "data": True})
            await self.cleanup()
        else:
            await self.client_send(ws, {"type": "server_connect", "data": False})
            await ws.close()

    async def client_connect(self, ws: wssp, data: dict):
        ws_id = str(ws.id)
        self._clients[ws_id] = ws
        data["target"] = ws_id
        await self.server_send({"type": "client_connect", "data": data})
        await self.cleanup()

    async def client_disconnect(self, ws: wssp, data: dict):
        ws_id = str(ws.id)
        if ws_id in self._clients:
            self._clients.pop(ws_id, None)

        if hasattr(ws, "group"):
            group: set = self._groups.get(ws.group)
            if ws_id in group:
                group.remove(ws_id)

            if not group:
                self._groups.pop(ws.group, None)

        await ws.close()

    async def client_connected(self, ws: wssp, data: dict):
        if self._servers.get(str(ws.id)):
            ws = self._clients.get(data.get("target"))
            if ws:
                ws_id = str(ws.id)
                user = data.pop("user", None) or "public"
                group: set = self._groups.get(user)
                if not group:
                    self._groups[user] = set([ws_id])
                else:
                    group.add(ws_id)

                old_group = getattr(ws, "group", None)
                if old_group:
                    group: set = self._groups.get(old_group)
                    if ws_id in group:
                        logging.info(f"Removing {ws_id} on group {old_group}")
                        group.remove(ws_id)

                ws.group = user
                ws.connected = True
                await self.client_send(ws, {"type": "client_connected", "data": data})

    async def notify_all(self, ws: wssp, data: dict):
        if self._servers.get(str(ws.id)):
            for clt in self._clients.copy().values():
                await self.client_send(clt, data)

    async def notify_client(self, ws: wssp, data: dict):
        ws_id = str(ws.id)
        if self._servers.get(ws_id) or getattr(ws, "connected", None):
            target = data.get("target") or ws_id
            if target:
                client = self._clients.get(target)
                if client:
                    await self.client_send(client, data.get("data") or {})

    async def notify_group(self, ws: wssp, data: dict):
        if self._servers.get(str(ws.id)) or getattr(ws, "connected", None):
            group = None
            target = data.get("target") or "public"
            client = self._clients.get(target)
            if client and hasattr(client, "group"):
                group: set = self._groups.get(client.group)
            else:
                group: set = self._groups.get(target)

            if group:
                data = data.get("data") or {}

                for clt in group.copy():
                    clt = self._clients.get(clt)
                    if clt:
                        await self.client_send(clt, data)

    async def consume(self, ws: wssp):
        try:
            async for event in ws:
                ev: dict = loads(event)
                method = self.method.get(ev["type"])
                if method:
                    await method(ws, ev.get("data") or {})
        except ConnectionClosed:
            await self.closed(ws)

    async def apis(self, path, headers):
        if path == "/healthz":
            return http.HTTPStatus.OK, [], b"OK\n"
        if path == "/hash":
            return (
                http.HTTPStatus.OK,
                [],
                bcrypt.hashpw(headers.get("pass").encode("utf-8"), bcrypt.gensalt())
                .hex()
                .encode(),
            )
        if path == "/terminate":
            loop = asyncio.get_running_loop()
            loop.call_later(1, sys.exit, 69)
            return http.HTTPStatus.OK, [], b"Terminating\n"

    async def closed(self, ws: wssp):
        ws_id = str(ws.id)
        if ws:
            logging.info(f"socket [{ws_id}] already closed!")
            self._clients.pop(ws_id, None)
            self._servers.pop(ws_id, None)

            ws_group = getattr(ws, "group", None)
            if ws_group:
                group: set = self._groups.get(ws_group)
                if group and ws_id in group:
                    group.remove(ws_id)

                if not group:
                    self._groups.pop(ws_group, None)

    def serve(self, *args, **kwargs):
        return websockets.serve(
            self.consume,
            *args,
            process_request=self.apis,
            logger=LoggerAdapter(logging.getLogger("websockets.server"), None),
            **kwargs,
        )
