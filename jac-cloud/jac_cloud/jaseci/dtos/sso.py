"""Jaseci SSO DTOs."""

from pydantic import BaseModel


class AttachSSO(BaseModel):
    """Attach SSO Request Model."""

    platform: str
    id: str
    email: str


class DetachSSO(BaseModel):
    """Attach SSO Request Model."""

    platform: str
