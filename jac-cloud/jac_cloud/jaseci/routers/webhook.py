"""Webhook APIs."""

from typing import cast

from bson import ObjectId

from fastapi import APIRouter, Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import ORJSONResponse

from passlib.hash import pbkdf2_sha512

from ..dtos import GenerateKey
from ..models import User, Webhook
from ..security import (
    authenticator,
    create_code,
    create_token,
    invalidate_token,
    verify_code,
)

router = APIRouter(prefix="/webhook", tags=["webhook"])


@router.post(
    "/generate-key", status_code=status.HTTP_201_CREATED, dependencies=authenticator
)
def generate_key(req: Request, gen_key: GenerateKey) -> ORJSONResponse:
    """Generate key API."""
    root_id: ObjectId = req._user.root_id  # type: ignore[attr-defined]

    user: BaseUser = User.Collection.find_by_email(req.email)  # type: ignore
    if not user or not pbkdf2_sha512.verify(req.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid Email/Password!")

    if RESTRICT_UNVERIFIED_USER and not user.is_activated:
        User.send_verification_code(create_code(user.id), req.email)
        raise HTTPException(
            status_code=400,
            detail="Account not yet verified! Resending verification code...",
        )

    user_json = user.serialize()
    token = create_token(user_json)
    return ORJSONResponse(content={"token": 1, "user": 1})
