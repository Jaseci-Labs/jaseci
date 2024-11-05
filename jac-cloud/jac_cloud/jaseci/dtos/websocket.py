"""Jaseci SSO DTOs."""

from typing import Annotated, Any, Literal, Union

from annotated_types import Len

from pydantic import BaseModel, Field


class ConnectionEvent(BaseModel):
    """Connection Event Model."""

    type: Literal["connection"]


class WalkerEventData(BaseModel):
    """Walker Event Data Model."""

    walker: str
    node: str | None = None
    context: dict[str, Any]


class WalkerEvent(BaseModel):
    """Walker Event Model."""

    type: Literal["walker"]
    data: WalkerEventData
    response: bool = False


class UserEvent(BaseModel):
    """Walker Event Model."""

    type: Literal["user"]
    root_ids: Annotated[list[str], Len(min_length=1)]
    data: dict


class ChannelEvent(BaseModel):
    """Walker Event Model."""

    type: Literal["channel"]
    channel_ids: Annotated[list[str], Len(min_length=1)]
    data: dict


class WebSocketEvent(BaseModel):
    """WebSocket Event."""

    event: Annotated[
        Union[ConnectionEvent, WalkerEvent, UserEvent, ChannelEvent],
        Field(discriminator="type"),
    ]
