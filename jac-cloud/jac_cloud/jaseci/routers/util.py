"""Jac Cloud Utils APIs."""

from typing import Annotated, Literal

from fastapi import APIRouter, Query, Request, status
from fastapi.responses import ORJSONResponse

from jac_cloud.core.architype import NodeAnchor
from jac_cloud.core.context import JaseciContext

from jaclang.plugin.feature import JacFeature as Jac

from ..security import authenticator

router = APIRouter(prefix="/util", tags=["Utility APIs"])


@router.get("/info", status_code=status.HTTP_200_OK)
async def info() -> ORJSONResponse:
    """Healthz API."""
    return ORJSONResponse(Jac.info())


@router.get(
    "/get_architypes", status_code=status.HTTP_200_OK, dependencies=authenticator
)
async def get_architypes(
    req: Request,
    type: Annotated[
        list[Literal["node", "edge", "walker", "object"]] | None, Query()
    ] = None,
    detailed: bool = False,
) -> ORJSONResponse:
    """Healthz API."""
    jctx = JaseciContext.create(req, None)

    archs = Jac.get_architypes(type=type, detailed=detailed)

    for key, dval in archs.items():
        jctx.clean_response(key, dval, archs)

    jctx.close()

    return ORJSONResponse(archs)


@router.get(
    "/traverse_node", status_code=status.HTTP_200_OK, dependencies=authenticator
)
async def traverse_node(
    req: Request,
    node: Annotated[str | None, Query()] = None,
    detailed: bool = False,
    show_edges: bool = False,
    node_types: Annotated[list[str] | None, Query()] = None,
    edge_types: Annotated[list[str] | None, Query()] = None,
) -> ORJSONResponse:
    """Healthz API."""
    jctx = JaseciContext.create(req, None)

    anchor = None
    if node and (_anchor := NodeAnchor.ref(node)).architype:
        anchor = _anchor

    archs = Jac.traverse_node(
        node=anchor,
        detailed=detailed,
        show_edges=show_edges,
        node_types=node_types,
        edge_types=edge_types,
    )

    for key, dval in archs.items():
        jctx.clean_response(key, dval, archs)

    jctx.close()

    return ORJSONResponse(archs)
