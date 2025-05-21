"""SSO APIs."""

from os import getenv
from typing import Any, cast

from asyncer import syncify

from bson import ObjectId

from fastapi import APIRouter, Request, Response
from fastapi.exceptions import HTTPException
from fastapi.responses import ORJSONResponse

from fastapi_sso.sso.base import OpenID, SSOBase
from fastapi_sso.sso.facebook import FacebookSSO
from fastapi_sso.sso.fitbit import FitbitSSO
from fastapi_sso.sso.github import GithubSSO
from fastapi_sso.sso.gitlab import GitlabSSO
from fastapi_sso.sso.kakao import KakaoSSO
from fastapi_sso.sso.line import LineSSO
from fastapi_sso.sso.linkedin import LinkedInSSO
from fastapi_sso.sso.microsoft import MicrosoftSSO
from fastapi_sso.sso.naver import NaverSSO
from fastapi_sso.sso.notion import NotionSSO
from fastapi_sso.sso.twitter import TwitterSSO
from fastapi_sso.sso.yandex import YandexSSO

from pymongo.errors import ConnectionFailure, DuplicateKeyError, OperationFailure

from ..dtos import AttachSSO, DetachSSO
from ..models import NO_PASSWORD, User as BaseUser
from ..security import authenticator, create_code, create_token
from ..sso import AppleSSO, GoogleSSO
from ..utils import logger
from ...core.archetype import BulkWrite, NodeAnchor

router = APIRouter(prefix="/sso", tags=["SSO APIs"])

User = BaseUser.model()  # type: ignore[misc]

CUSTOM_PLATFORMS = [AppleSSO]
SUPPORTED_PLATFORMS: dict[str, type[SSOBase]] = {
    "APPLE": AppleSSO,
    "FACEBOOK": FacebookSSO,
    "FITBIT": FitbitSSO,
    "GITHUB": GithubSSO,
    "GITLAB": GitlabSSO,
    "GOOGLE": GoogleSSO,
    "GOOGLE_ANDROID": GoogleSSO,
    "GOOGLE_IOS": GoogleSSO,
    "KAKAO": KakaoSSO,
    "LINE": LineSSO,
    "LINKEDIN": LinkedInSSO,
    "MICROSOFT": MicrosoftSSO,
    "NAVER": NaverSSO,
    "NOTION": NotionSSO,
    "TWITTER": TwitterSSO,
    "YANDEX": YandexSSO,
}

SSO: dict[str, SSOBase] = {}
SSO_HOST = getenv("SSO_HOST", "http://localhost:8000/sso")

for platform, cls in SUPPORTED_PLATFORMS.items():
    if client_id := getenv(f"SSO_{platform}_CLIENT_ID"):
        options: dict[str, Any] = {
            "client_id": client_id,
            "client_secret": getenv(f"SSO_{platform}_CLIENT_SECRET"),
        }

        if base_endpoint_url := getenv(f"SSO_{platform}_BASE_ENDPOINT_URL"):
            options["base_endpoint_url"] = base_endpoint_url

        if tenant := getenv(f"SSO_{platform}_TENANT"):
            options["tenant"] = tenant

        if allow_insecure_http := getenv(f"SSO_{platform}_ALLOW_INSECURE_HTTP"):
            options["allow_insecure_http"] = allow_insecure_http == "true"

        if cls in CUSTOM_PLATFORMS:
            options["platform"] = platform

        SSO[platform.lower()] = cls(**options)


@router.get("/{platform}/{operation}")
def sso_operation(
    request: Request,
    platform: str,
    operation: str,
    redirect_uri: str | None = None,
    state: str | None = None,
) -> Response:
    """SSO Login API."""
    if sso := SSO.get(platform):
        with sso:
            params = request.query_params._dict
            return syncify(sso.get_login_redirect)(
                redirect_uri=params.pop("redirect_uri", None)
                or f"{SSO_HOST}/{platform}/{operation}/callback",
                state=params.pop("state", None),
                params=params,
            )
    return ORJSONResponse({"message": "Feature not yet implemented!"}, 501)


@router.get("/{platform}/{operation}/callback")
def sso_callback(
    request: Request, platform: str, operation: str, redirect_uri: str | None = None
) -> Response:
    """SSO Login API."""
    if sso := SSO.get(platform):
        with sso:
            if open_id := syncify(sso.verify_and_process)(
                request,
                redirect_uri=redirect_uri
                or f"{SSO_HOST}/{platform}/{operation}/callback",
            ):
                match operation:
                    case "login":
                        return login(platform, open_id)
                    case "register":
                        return register(platform, open_id)
                    case "attach":
                        return attach(platform, open_id)
                    case _:
                        pass

    return ORJSONResponse({"message": "Feature not yet implemented!"}, 501)


@router.post("/attach", dependencies=authenticator)
def sso_attach(request: Request, attach_sso: AttachSSO) -> ORJSONResponse:
    """Generate token from user."""
    if SSO.get(attach_sso.platform):
        if User.Collection.find_one(
            {
                "$or": [
                    {f"sso.{platform}.id": attach_sso.id},
                    {f"sso.{platform}.email": attach_sso.email},
                ]
            }
        ):
            return ORJSONResponse({"message": "Already Attached!"}, 403)

        User.Collection.update_one(
            {"_id": ObjectId(request._user.id)},
            {
                "$set": {
                    f"sso.{attach_sso.platform}": {
                        "id": attach_sso.id,
                        "email": attach_sso.email,
                    }
                }
            },
        )

        return ORJSONResponse({"message": "Successfully Updated SSO!"}, 200)
    return ORJSONResponse({"message": "Feature not yet implemented!"}, 501)


@router.delete("/detach", dependencies=authenticator)
def sso_detach(request: Request, detach_sso: DetachSSO) -> ORJSONResponse:
    """Generate token from user."""
    if SSO.get(detach_sso.platform):
        User.Collection.update_one(
            {"_id": ObjectId(request._user.id)},
            {"$unset": {f"sso.{detach_sso.platform}": 1}},
        )
        return ORJSONResponse({"message": "Successfully Updated SSO!"}, 200)
    return ORJSONResponse({"message": "Feature not yet implemented!"}, 501)


def get_token(user: User) -> ORJSONResponse:  # type: ignore
    """Generate token from user."""
    user_json = user.serialize()  # type: ignore[attr-defined]
    token = create_token(user_json)

    return ORJSONResponse(content={"token": token, "user": user_json})


def login(platform: str, open_id: OpenID) -> Response:
    """Login user method."""
    if user := BaseUser.Collection.find_one(
        {
            "$or": [
                {f"sso.{platform}.id": open_id.id},
                {f"sso.{platform}.email": open_id.email},
            ]
        }
    ):
        if not user.is_activated:
            User.send_verification_code(create_code(ObjectId(user.id)), user.email)
            raise HTTPException(
                status_code=400,
                detail="Account not yet verified! Resending verification code...",
            )

        return get_token(user)
    return ORJSONResponse({"message": "Not Existing!"}, 403)


def register(platform: str, open_id: OpenID) -> Response:
    """Register user method."""
    from ...core.archetype import Root

    if user := User.Collection.find_one(
        {
            "$or": [
                {f"sso.{platform}.id": open_id.id},
                {f"sso.{platform}.email": open_id.email},
            ]
        }
    ):
        return get_token(cast(User, user))  # type: ignore

    with User.Collection.get_session() as session, session.start_transaction():
        retry = 0
        while True:
            try:
                if not User.Collection.update_one(
                    {"email": open_id.email},
                    {
                        "$set": {
                            f"sso.{platform}": {
                                "id": open_id.id,
                                "email": open_id.email,
                            },
                            "is_activated": True,
                        }
                    },
                    session=session,
                ).modified_count:
                    root = Root().__jac__  # type: ignore[attr-defined]
                    ureq: dict[str, object] = User.register_type()(
                        email=open_id.email,
                        password=NO_PASSWORD,
                        **User.sso_mapper(open_id),
                    ).obfuscate()
                    ureq["root_id"] = root.id
                    ureq["is_activated"] = True
                    ureq["sso"] = {platform: {"id": open_id.id, "email": open_id.email}}
                    NodeAnchor.Collection.insert_one(root.serialize(), session)
                    User.Collection.insert_one(ureq, session=session)
                BulkWrite.commit(session)
                return login(platform, open_id)
            except DuplicateKeyError:
                raise HTTPException(409, "Already Exists!")
            except (ConnectionFailure, OperationFailure) as ex:
                if (
                    ex.has_error_label("TransientTransactionError")
                    and retry <= BulkWrite.SESSION_MAX_TRANSACTION_RETRY
                ):
                    retry += 1
                    logger.exception(
                        "Error executing bulk write! "
                        f"Retrying [{retry}/{BulkWrite.SESSION_MAX_TRANSACTION_RETRY}] ..."
                    )
                    continue
                logger.exception(
                    f"Error executing bulk write after max retry [{BulkWrite.SESSION_MAX_TRANSACTION_RETRY}] !"
                )
                raise
            except Exception:
                logger.exception("Error executing bulk write!")
                raise
    return ORJSONResponse({"message": "Registration Failed!"}, 409)


def attach(platform: str, open_id: OpenID) -> Response:
    """Return openid ."""
    if User.Collection.find_one(
        {
            "$or": [
                {f"sso.{platform}.id": open_id.id},
                {f"sso.{platform}.email": open_id.email},
            ]
        }
    ):
        return ORJSONResponse({"message": "Already Attached!"}, 403)

    return ORJSONResponse(
        {"platform": platform, "id": open_id.id, "email": open_id.email}, 200
    )
