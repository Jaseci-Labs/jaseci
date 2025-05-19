"""User APIs."""

from os import getenv

from fastapi import APIRouter, Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import ORJSONResponse

from passlib.hash import pbkdf2_sha512

from pymongo.errors import ConnectionFailure, DuplicateKeyError, OperationFailure

from ..dtos import (
    UserChangePassword,
    UserForgotPassword,
    UserRequest,
    UserResetPassword,
    UserVerification,
)
from ..models import User as BaseUser
from ..security import (
    authenticator,
    create_code,
    create_token,
    invalidate_token,
    verify_code,
)
from ..utils import Emailer, log_entry, log_exit, logger
from ...core.archetype import BulkWrite, NodeAnchor


RESTRICT_UNVERIFIED_USER = getenv("RESTRICT_UNVERIFIED_USER") == "true"
router = APIRouter(prefix="/user", tags=["User APIs"])

User = BaseUser.model()  # type: ignore[misc]


@router.post("/register", status_code=status.HTTP_200_OK)
def register(req: User.register_type()) -> ORJSONResponse:  # type: ignore
    """Register user API."""
    from ...core.archetype import Root

    log = log_entry("register", req.email, req.printable())

    with User.Collection.get_session() as session, session.start_transaction():
        root = Root().__jac__  # type: ignore[attr-defined]

        req_obf: dict = req.obfuscate()
        req_obf["root_id"] = root.id
        req_obf["is_admin"] = False
        is_activated = req_obf["is_activated"] = not Emailer.has_client()

        retry = 0
        while True:
            try:
                NodeAnchor.Collection.insert_one(root.serialize(), session)
                if id := (
                    User.Collection.insert_one(req_obf, session=session)
                ).inserted_id:
                    BulkWrite.commit(session)
                    if not is_activated:
                        User.send_verification_code(create_code(id), req.email)
                    resp = {"message": "Successfully Registered!"}
                    log_exit(resp, log)
                    return ORJSONResponse(resp, 201)
                raise SystemError("Can't create System Admin!")
            except DuplicateKeyError:
                raise HTTPException(409, "Already Exists!")
            except (ConnectionFailure, OperationFailure) as ex:
                if (
                    ex.has_error_label("TransientTransactionError")
                    and retry <= BulkWrite.SESSION_MAX_TRANSACTION_RETRY
                ):
                    retry += 1
                    logger.error(
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

    resp = {"message": "Registration Failed!"}
    log_exit(resp, log)
    return ORJSONResponse(resp, 409)


@router.post(
    "/send-verification-code",
    status_code=status.HTTP_200_OK,
    dependencies=authenticator,
)
def send_verification_code(request: Request) -> ORJSONResponse:
    """Verify user API."""
    user: BaseUser = request._user  # type: ignore[attr-defined]
    if user.is_activated:
        return ORJSONResponse({"message": "Account is already verified!"}, 400)
    else:
        User.send_verification_code(create_code(user.id), user.email)
        return ORJSONResponse({"message": "Successfully sent verification code!"}, 200)


@router.post("/verify")
def verify(req: UserVerification) -> ORJSONResponse:
    """Verify user API."""
    if (user_id := verify_code(req.code)) and User.Collection.update_by_id(
        user_id, {"$set": {"is_activated": True}}
    ):
        return ORJSONResponse({"message": "Successfully Verified!"}, 200)

    return ORJSONResponse({"message": "Verification Failed!"}, 403)


@router.post("/login")
def login(req: UserRequest) -> ORJSONResponse:
    """Login user API."""
    log = log_entry("login", req.email, {"email": req.email, "password": "****"})

    user: BaseUser = User.Collection.find_by_email(req.email)  # type: ignore
    if not user or not pbkdf2_sha512.verify(req.password, user.password):
        resp = {"message": "Invalid Email/Password!"}
        log_exit(resp, log)
        return ORJSONResponse(resp, 400)

    if RESTRICT_UNVERIFIED_USER and not user.is_activated:
        User.send_verification_code(create_code(user.id), req.email)
        raise HTTPException(
            status_code=400,
            detail="Account not yet verified! Resending verification code...",
        )

    user_json = user.serialize()
    token = create_token(user_json)

    log_exit({"token": "****", "user": {**user_json, "state": "****"}}, log)
    return ORJSONResponse(content={"token": token, "user": user_json})


@router.post(
    "/change_password", status_code=status.HTTP_200_OK, dependencies=authenticator
)
def change_password(request: Request, ucp: UserChangePassword) -> ORJSONResponse:  # type: ignore
    """Register user API."""
    user: BaseUser | None = getattr(request, "_user", None)
    if user:
        with_pass = User.Collection.find_by_email(user.email)
        if (
            with_pass
            and pbkdf2_sha512.verify(ucp.old_password, with_pass.password)
            and User.Collection.update_one(
                {"_id": user.id},
                {"$set": {"password": pbkdf2_sha512.hash(ucp.new_password).encode()}},
            )
        ):
            invalidate_token(user.id)
            return ORJSONResponse({"message": "Successfully Updated!"}, 200)
    return ORJSONResponse({"message": "Update Failed!"}, 403)


@router.post("/forgot_password", status_code=status.HTTP_200_OK)
def forgot_password(ufp: UserForgotPassword) -> ORJSONResponse:
    """Forgot password API."""
    user = User.Collection.find_by_email(ufp.email)
    if isinstance(user, User):
        User.send_reset_code(create_code(user.id, True), user.email)
        return ORJSONResponse({"message": "Reset password email sent!"}, 200)
    else:
        return ORJSONResponse({"message": "Failed to process forgot password!"}, 403)


@router.post("/reset_password", status_code=status.HTTP_200_OK)
def reset_password(urp: UserResetPassword) -> ORJSONResponse:
    """Reset password API."""
    if (user_id := verify_code(urp.code, True)) and User.Collection.update_by_id(
        user_id,
        {
            "$set": {
                "password": pbkdf2_sha512.hash(urp.password).encode(),
                "is_activated": True,
            }
        },
    ):
        invalidate_token(user_id)
        return ORJSONResponse({"message": "Password reset successfully!"}, 200)

    return ORJSONResponse({"message": "Failed to reset password!"}, 403)
