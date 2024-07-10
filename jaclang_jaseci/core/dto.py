"""Jaseci DTOs."""

from pydantic import BaseModel, EmailStr


class UserRequest(BaseModel):
    """User Creation Request Model."""

    email: EmailStr
    password: str


class UserVerification(BaseModel):
    """User Verification Request Model."""

    code: str


class AttachSSO(BaseModel):
    """Attach SSO Request Model."""

    platform: str
    id: str
    email: str


class DetachSSO(BaseModel):
    """Attach SSO Request Model."""

    platform: str
