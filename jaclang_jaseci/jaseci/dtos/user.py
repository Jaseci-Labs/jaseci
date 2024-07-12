"""Jaseci User DTOs."""

from pydantic import BaseModel, EmailStr


class UserRequest(BaseModel):
    """User Creation Request Model."""

    email: EmailStr
    password: str


class UserVerification(BaseModel):
    """User Verification Request Model."""

    code: str
