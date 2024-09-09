"""Healthz APIs."""

from fastapi import APIRouter, Response, status

router = APIRouter(prefix="/healthz", tags=["monitoring"])


@router.get("", status_code=status.HTTP_200_OK)
async def healthz() -> Response:
    """Healthz API."""
    return Response()
