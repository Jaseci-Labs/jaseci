"""Jaseci User DTOs."""

from typing import Literal

from annotated_types import Len

from pydantic import BaseModel, Field, StringConstraints

from typing_extensions import Annotated


class Expiration(BaseModel):
    """Key Expiration."""

    count: Annotated[int, Field(strict=True, gt=0, default=60)] = 60
    interval: Literal["seconds", "minutes", "hours", "days"] = "days"


class GenerateKey(BaseModel):
    """User Creation Request Model."""

    name: Annotated[str, StringConstraints(min_length=1)]
    walkers: list[str] = Field(default_factory=list)
    nodes: list[str] = Field(default_factory=list)
    expiration: Expiration = Field(default_factory=Expiration)


class KeyIDs(BaseModel):
    """User Creation Request Model."""

    ids: Annotated[list[str], Len(min_length=1)]
