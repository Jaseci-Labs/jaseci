"""Jaseci User DTOs."""

from typing import Literal

from annotated_types import Len

from pydantic import BaseModel, Field

from typing_extensions import Annotated


class Expiration(BaseModel):
    """Key Expiration."""

    count: Annotated[int, Field(strict=True, gt=0, default=60)] = 60
    interval: Literal["seconds", "minutes", "hours", "days"] = "days"


class GenerateKey(BaseModel):
    """User Creation Request Model."""

    walkers: Annotated[list[str], Len(min_length=1)]
    nodes: list[str] = Field(default_factory=list)
    expiration: Expiration = Field(default_factory=Expiration)
