"""Jaseci Securities."""

from os import getenv
from typing import Any

from bson import ObjectId

from fastapi import Depends, Request
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer

from jwt import decode, encode

from ..datasources.redis import CodeRedis, TokenRedis
from ..models.user import User as BaseUser
from ..utils import logger, random_string, utc_timestamp
from ...core.architype import NodeAnchor


TOKEN_SECRET = getenv("TOKEN_SECRET", random_string(50))
TOKEN_ALGORITHM = getenv("TOKEN_ALGORITHM", "HS256")
VERIFICATION_CODE_TIMEOUT = int(getenv("VERIFICATION_CODE_TIMEOUT") or "24")
RESET_CODE_TIMEOUT = int(getenv("RESET_CODE_TIMEOUT") or "24")
TOKEN_TIMEOUT = int(getenv("TOKEN_TIMEOUT") or "12")
User = BaseUser.model()


def encrypt(data: dict) -> str:
    """Encrypt data."""
    return encode(data, key=TOKEN_SECRET, algorithm=TOKEN_ALGORITHM)


def decrypt(token: str) -> dict | None:
    """Decrypt data."""
    try:
        return decode(token, key=TOKEN_SECRET, algorithms=[TOKEN_ALGORITHM])
    except Exception:
        logger.exception("Token is invalid!")
        return None


def create_code(user_id: ObjectId, reset: bool = False) -> str:
    """Generate Verification Code."""
    verification = encrypt(
        {
            "user_id": str(user_id),
            "reset": reset,
            "expiration": utc_timestamp(
                hours=RESET_CODE_TIMEOUT if reset else VERIFICATION_CODE_TIMEOUT
            ),
        }
    )
    if CodeRedis.hset(key=verification, data=True):
        return verification
    raise HTTPException(500, "Verification Creation Failed!")


def verify_code(code: str, reset: bool = False) -> ObjectId | None:
    """Verify Code."""
    decrypted = decrypt(code)
    if (
        decrypted
        and decrypted["reset"] == reset
        and decrypted["expiration"] > utc_timestamp()
        and CodeRedis.hget(key=code)
    ):
        CodeRedis.hdelete(code)
        return ObjectId(decrypted["user_id"])
    return None


def create_token(user: dict[str, Any]) -> str:
    """Generate token for current user."""
    user["expiration"] = utc_timestamp(hours=TOKEN_TIMEOUT)
    user["state"] = random_string(8)
    token = encrypt(user)
    if TokenRedis.hset(f"{user['id']}:{token}", True):
        return token
    raise HTTPException(500, "Token Creation Failed!")


def invalidate_token(user_id: ObjectId) -> None:
    """Invalidate token of current user."""
    TokenRedis.hdelete_rgx(f"{user_id}:*")


def authenticate(request: Request) -> None:
    """Authenticate current request and attach authenticated user and their root."""
    authorization = request.headers.get("Authorization")
    if authorization and authorization.lower().startswith("bearer"):
        token = authorization[7:]
        decrypted = decrypt(token)
        if (
            decrypted
            and decrypted["expiration"] > utc_timestamp()
            and TokenRedis.hget(f"{decrypted['id']}:{token}")
            and (user := User.Collection.find_by_id(decrypted["id"]))
            and (root := NodeAnchor.Collection.find_by_id(user.root_id))
        ):
            request._user = user  # type: ignore[attr-defined]
            request._root = root  # type: ignore[attr-defined]
            return

    raise HTTPException(status_code=401)


authenticator = [Depends(HTTPBearer()), Depends(authenticate)]
