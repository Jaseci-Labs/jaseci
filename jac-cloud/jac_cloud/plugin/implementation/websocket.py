"""Websocket Handler."""

from contextlib import suppress
from dataclasses import MISSING, dataclass
from os import getenv
from traceback import format_exception
from typing import Any, Iterable, cast
from uuid import uuid4

from anyio import create_task_group, to_thread
from anyio.abc import TaskGroup

from asyncer import syncify

from broadcaster import Broadcast

from fastapi import APIRouter, WebSocket

from jaclang.plugin.feature import JacFeature as Jac

from pydantic import ValidationError

from starlette.websockets import WebSocketDisconnect, WebSocketState

from ...core.architype import Anchor, NodeAnchor, WalkerAnchor
from ...core.context import JaseciContext, PUBLIC_ROOT
from ...jaseci.dtos import (
    ChannelEvent,
    ConnectionEvent,
    UserEvent,
    WalkerEvent,
    WalkerEventData,
    WebSocketEvent,
)
from ...jaseci.security import authenticate_websocket
from ...jaseci.utils import utc_timestamp

websocket_router = APIRouter(prefix="/websocket", tags=["walker"])
websocket_events: dict[str, dict[str, Any]] = {}


@dataclass(frozen=True)
class Socket:
    """Client Handler."""

    root: NodeAnchor
    websocket: WebSocket
    channel_id: str


class WebSocketManager:
    """WebSocket Manager."""

    def __init__(self) -> None:
        """Initialize."""
        self.broadcaster: Broadcast | None = (
            Broadcast(socket_redis_host)
            if (socket_redis_host := getenv("SOCKET_REDIS_HOST"))
            else None
        )
        self.user_websockets: dict[NodeAnchor, set[Socket]] = {}
        self.channel_websockets: dict[str, set[Socket]] = {}
        self.websocket_clients: dict[int, Socket] = {}

    async def connect(
        self, task_group: TaskGroup, websocket: WebSocket, channel_id: str | None
    ) -> None:
        """Connect Websocket."""
        await websocket.accept()

        root: NodeAnchor = websocket._root  # type: ignore[attr-defined]
        channel_id = websocket._channel_id = (  # type: ignore[attr-defined]
            channel_id or f"{utc_timestamp()}:{uuid4()}"
        )

        socket = Socket(root, websocket, channel_id)

        if root not in self.user_websockets:
            self.user_websockets[root] = set()

        if channel_id not in self.channel_websockets:
            self.channel_websockets[channel_id] = set()

        self.user_websockets[root].add(socket)
        self.channel_websockets[channel_id].add(socket)
        self.websocket_clients[id(websocket)] = socket

        await connection_execution(websocket)

        if broadcaster := self.broadcaster:

            async def run_broadcast_reciever() -> None:
                async with broadcaster.subscribe(channel=socket.channel_id) as sub:
                    with suppress(Exception):
                        while True:
                            await socket.websocket.send_json(await sub.get())
                task_group.cancel_scope.cancel()

            task_group.start_soon(run_broadcast_reciever)

    async def disconnect(self, task_group: TaskGroup, websocket: WebSocket) -> None:
        """Disconnect Websocket."""
        if websocket.client_state is WebSocketState.CONNECTED:
            await websocket.close()

        root: NodeAnchor = websocket._root  # type: ignore[attr-defined]
        channel_id: str = websocket._channel_id  # type: ignore[attr-defined]

        if socket := self.websocket_clients.pop(id(websocket), None):
            self.user_websockets[root].remove(socket)
            self.channel_websockets[channel_id].remove(socket)

        task_group.cancel_scope.cancel()

    def notify_self(self, data: dict) -> None:
        """Notify self client."""
        if isinstance(socket := JaseciContext.get().connection, WebSocket):
            syncify(socket.send_json)(data)

    def notify_clients(self, socket_ids: Iterable[int], data: dict) -> None:
        """Notify clients associated with target root."""
        for socket_id in socket_ids:
            if socket := self.websocket_clients.get(socket_id):
                syncify(socket.websocket.send_json)(data)

    def notify_users(self, roots: Iterable[NodeAnchor], data: dict) -> None:
        """Notify clients associated with target root."""
        for root in roots:
            if sockets := self.user_websockets.get(root):
                for socket in sockets:
                    syncify(socket.websocket.send_json)(data)

    def notify_channels(self, channel_ids: Iterable[str], data: dict) -> None:
        """Notify clients associated with target root."""
        for channel_id in channel_ids:
            if sockets := self.channel_websockets.get(channel_id):
                for socket in sockets:
                    syncify(socket.websocket.send_json)(data)


def walker_execution(websocket: WebSocket, event: WalkerEventData) -> dict:
    """Websocket event sychronizer."""
    if walker_event := websocket_events.get(even_walker := event.walker):
        if walker_event["auth"] and websocket._root is PUBLIC_ROOT:  # type: ignore[attr-defined]
            return {"error": f"Event {even_walker} requires to be authenticated!"}
        elif not walker_event["auth"] and websocket._root is not PUBLIC_ROOT:  # type: ignore[attr-defined]
            return {"error": f"Event {even_walker} requires to be unauthenticated!"}

        walker: type = walker_event["type"]
        try:
            payload = walker_event["model"](**event.context).__dict__
        except ValidationError:
            raise

        jctx = JaseciContext.create(
            websocket, NodeAnchor.ref(event.node) if event.node else None
        )

        wlk: WalkerAnchor = walker(**payload).__jac__
        if Jac.check_read_access(jctx.entry_node):
            Jac.spawn_call(wlk.architype, jctx.entry_node.architype)
            jctx.close()

            if jctx.custom is not MISSING:
                return jctx.custom

            return jctx.response(wlk.returns)
        else:
            jctx.close()
            return {
                "error": f"You don't have access on target entry{cast(Anchor, jctx.entry_node).ref_id}!"
            }
    else:
        return {"error": "Invalid request! Please use valid walker event!"}


async def user_execution(websocket: WebSocket, event: UserEvent) -> None:
    """User event execution."""
    for root_id in event.root_ids:
        if sockets := WEBSOCKET_MANAGER.user_websockets.get(NodeAnchor.ref(root_id)):
            for socket in sockets:
                await socket.websocket.send_json(event.data)


async def channel_execution(websocket: WebSocket, event: ChannelEvent) -> None:
    """Channel event execution."""
    for channel_id in event.channel_ids:
        if sockets := WEBSOCKET_MANAGER.channel_websockets.get(channel_id):
            for socket in sockets:
                await socket.websocket.send_json(event.data)


async def connection_execution(websocket: WebSocket) -> None:
    """Websocket connection info."""
    await websocket.send_json(
        {
            "type": "connection",
            "data": {
                "client_id": id(websocket),
                "root_id": websocket._root.ref_id,  # type: ignore[attr-defined]
                "channel_id": websocket._channel_id,  # type: ignore[attr-defined]
            },
        }
    )


@websocket_router.websocket("")
async def websocket_endpoint(
    websocket: WebSocket, channel_id: str | None = None
) -> None:
    """Websocket Endpoint."""
    if not websocket_events:
        await websocket.close()
        return

    if not authenticate_websocket(websocket):
        websocket._root = PUBLIC_ROOT  # type: ignore[attr-defined]

    async with create_task_group() as task_group:
        await WEBSOCKET_MANAGER.connect(task_group, websocket, channel_id)
        while True:
            try:
                event = WebSocketEvent(event=await websocket.receive_json()).event
                match event:
                    case WalkerEvent():
                        resp = await to_thread.run_sync(
                            walker_execution, websocket, event.data
                        )
                        if event.response:
                            await websocket.send_json(resp)
                    case UserEvent():
                        await user_execution(websocket, event)
                    case ChannelEvent():
                        await channel_execution(websocket, event)
                    case ConnectionEvent():
                        await connection_execution(websocket)
                    case _:
                        await websocket.send_json({"error": "Not a valid event!"})
            except ValidationError as e:
                await websocket.send_json({"error": e.errors()})
            except WebSocketDisconnect:
                await WEBSOCKET_MANAGER.disconnect(task_group, websocket)
                break
            except Exception as e:
                match websocket.client_state:
                    case WebSocketState.CONNECTED:
                        await websocket.send_json({"error": format_exception(e)})
                    case WebSocketState.DISCONNECTED:
                        await WEBSOCKET_MANAGER.disconnect(task_group, websocket)
                        break
                    case _:
                        pass


WEBSOCKET_MANAGER = WebSocketManager()
