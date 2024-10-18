"""User APIs."""

from fastapi import APIRouter, Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import ORJSONResponse

from passlib.hash import pbkdf2_sha512

from ..dtos import GenerateKey
from ..models import Webhook
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
def generate_key(req: GenerateKey) -> ORJSONResponse:
    """Generate key API."""
    import pdb

    pdb.set_trace()
    return ORJSONResponse(content={"token": 1, "user": 1})
