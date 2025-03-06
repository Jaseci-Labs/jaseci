"""WebSocket APIs."""

from datetime import timedelta

from bson import ObjectId

from fastapi import APIRouter, Request, status
from fastapi.responses import ORJSONResponse

from pymongo.errors import ConnectionFailure, OperationFailure

from ..datasources.redis import WebSocketRedis
from ..dtos import Expiration, GenerateKey, KeyIDs
from ..models import WebSocket
from ..security import authenticator
from ..utils import logger, random_string, utc_datetime, utc_timestamp
from ...core.architype import BulkWrite

router = APIRouter(prefix="/websocket", tags=["WebSocket APIs"])


@router.get("", status_code=status.HTTP_200_OK, dependencies=authenticator)
def get(req: Request) -> ORJSONResponse:
    """Get keys API."""
    root_id: ObjectId = req._user.root_id  # type: ignore[attr-defined]

    return ORJSONResponse(
        content={
            "keys": [
                {
                    "id": str(key.id),
                    "name": key.name,
                    "root_id": str(key.root_id),
                    "walkers": key.walkers,
                    "nodes": key.nodes,
                    "expiration": key.expiration,
                    "key": key.key,
                }
                for key in WebSocket.Collection.find({"root_id": root_id})
            ]
        }
    )


@router.post(
    "/generate-key", status_code=status.HTTP_201_CREATED, dependencies=authenticator
)
def generate_key(req: Request, gen_key: GenerateKey) -> ORJSONResponse:
    """Generate key API."""
    root_id: ObjectId = req._user.root_id  # type: ignore[attr-defined]

    _exp: dict[str, int] = {gen_key.expiration.interval: gen_key.expiration.count}
    exp = utc_datetime(**_exp)

    websocket = WebSocket(
        name=gen_key.name,
        root_id=root_id,
        walkers=gen_key.walkers,
        nodes=gen_key.nodes,
        expiration=exp,
        key=f"{root_id}:{utc_timestamp()}:{random_string(32)}",
    )

    if (
        id := WebSocket.Collection.insert_one(websocket.__serialize__()).inserted_id
    ) and WebSocketRedis.hset(
        websocket.key,
        {
            "walkers": websocket.walkers,
            "nodes": websocket.nodes,
            "expiration": websocket.expiration.timestamp(),
        },
    ):
        return ORJSONResponse(
            content={"id": str(id), "name": websocket.name, "key": websocket.key},
            status_code=201,
        )

    return ORJSONResponse(
        content="Can't generate key at the moment. Please try again!", status_code=500
    )


@router.patch(
    "/extend/{id}", status_code=status.HTTP_201_CREATED, dependencies=authenticator
)
def extend(id: str, expiration: Expiration) -> ORJSONResponse:
    """Generate key API."""
    with WebSocket.Collection.get_session() as session, session.start_transaction():
        retry = 0
        max_retry = BulkWrite.SESSION_MAX_TRANSACTION_RETRY
        while retry <= max_retry:
            try:
                _id = ObjectId(id)
                if websocket := WebSocket.Collection.find_by_id(_id, session=session):
                    _exp: dict[str, int] = {expiration.interval: expiration.count}
                    websocket.expiration += timedelta(**_exp)

                    if WebSocket.Collection.update_by_id(
                        _id, {"$set": {"expiration": websocket.expiration}}, session
                    ).modified_count:
                        WebSocketRedis.hset(
                            websocket.key,
                            {
                                "walkers": websocket.walkers,
                                "nodes": websocket.nodes,
                                "expiration": websocket.expiration.timestamp(),
                            },
                        )
                        BulkWrite.commit(session)
                        return ORJSONResponse(
                            {"message": "Successfully Extended!"}, 200
                        )
                break
            except (ConnectionFailure, OperationFailure) as ex:
                if ex.has_error_label("TransientTransactionError"):
                    retry += 1
                    logger.error(
                        f"Error executing transaction! Retrying [{retry}/{max_retry}] ..."
                    )
                    continue
                logger.exception("Error executing transaction!")
                session.abort_transaction()
                break
            except Exception:
                logger.exception("Error executing transaction!")
                session.abort_transaction()
                break

    return ORJSONResponse(
        content="Can't extend key at the moment. Please try again!", status_code=500
    )


@router.delete("/delete", status_code=status.HTTP_200_OK, dependencies=authenticator)
def delete(key_ids: KeyIDs) -> ORJSONResponse:
    """Delete keys API."""
    with WebSocket.Collection.get_session() as session, session.start_transaction():
        retry = 0
        max_retry = BulkWrite.SESSION_MAX_TRANSACTION_RETRY
        while retry <= max_retry:
            try:
                ids = [ObjectId(id) for id in key_ids.ids]
                wss = WebSocket.Collection.find({"_id": {"$in": ids}})
                if WebSocket.Collection.delete(
                    {"_id": {"$in": ids}}, session
                ).deleted_count == len(key_ids.ids):
                    for ws in wss:
                        WebSocketRedis.hdelete(ws.key)
                    BulkWrite.commit(session)
                    return ORJSONResponse({"message": "Successfully Deleted!"}, 200)
                break
            except (ConnectionFailure, OperationFailure) as ex:
                if ex.has_error_label("TransientTransactionError"):
                    retry += 1
                    logger.error(
                        f"Error executing transaction! Retrying [{retry}/{max_retry}] ..."
                    )
                    continue
                logger.exception("Error executing transaction!")
                session.abort_transaction()
                break
            except Exception:
                logger.exception("Error executing transaction!")
                session.abort_transaction()
                break

    return ORJSONResponse(
        content="Error occured during deletion. Please try again!", status_code=500
    )
