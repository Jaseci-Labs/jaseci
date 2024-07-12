"""Healthz APIs."""

from fastapi import APIRouter, status

router = APIRouter(prefix="/healthz", tags=["monitoring"])


@router.get("", status_code=status.HTTP_200_OK)
async def healthz() -> bool:  # type: ignore
    """Healthz API."""
    return True
