"""Jaseci SSO DTOs."""

from typing import Annotated, Any, Literal, Union

from annotated_types import Len

from pydantic import BaseModel, Field


class ConnectionEvent(BaseModel):
    """Connection Event Model."""

    type: Literal["connection"] = "connection"


class WalkerEvent(BaseModel):
    """Walker Event Model."""

    type: Literal["walker"] = "walker"
    walker: str
    node: str | None = None
    response: bool = False
    context: dict[str, Any] = Field(default_factory=dict)


class UserEvent(BaseModel):
    """Walker Event Model."""

    type: Literal["user"] = "user"
    root_ids: Annotated[list[str], Len(min_length=1)]
    data: dict


class ChannelEvent(BaseModel):
    """Walker Event Model."""

    type: Literal["channel"] = "channel"
    channel_ids: Annotated[list[str], Len(min_length=1)]
    data: dict


class ClientEvent(BaseModel):
    """Walker Event Model."""

    type: Literal["client"] = "client"
    client_ids: Annotated[list[str], Len(min_length=1)]
    data: dict


class ChangeUserEvent(BaseModel):
    """Change User Event Model."""

    type: Literal["change_user"] = "change_user"
    token: str | None = None


class WebSocketEvent(BaseModel):
    """WebSocket Event."""

    instance_id: str | None = None
    event: Annotated[
        Union[
            ConnectionEvent,
            WalkerEvent,
            UserEvent,
            ChannelEvent,
            ClientEvent,
            ChangeUserEvent,
        ],
        Field(discriminator="type"),
    ]
