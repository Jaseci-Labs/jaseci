"""Jaseci User DTOs."""

from pydantic import BaseModel, EmailStr


class UserRequest(BaseModel):
    """User Creation Request Model."""

    email: EmailStr
    password: str


class UserChangePassword(BaseModel):
    """User Creation Request Model."""

    old_password: str
    new_password: str


class UserForgotPassword(BaseModel):
    """User Creation Request Model."""

    email: EmailStr


class UserResetPassword(BaseModel):
    """User Creation Request Model."""

    code: str
    password: str


class UserVerification(BaseModel):
    """User Verification Request Model."""

    code: str
