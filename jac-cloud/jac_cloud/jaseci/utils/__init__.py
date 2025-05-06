"""Jaseci Utilities."""

from datetime import datetime, timedelta, timezone
from functools import lru_cache
from io import StringIO
from random import choice
from string import ascii_letters, digits

from fastapi import FastAPI, Response

from yaml import dump as ydump

from .logger import log_dumps, log_entry, log_exit, logger
from .mail import Emailer, SendGridEmailer


def random_string(length: int) -> str:
    """Generate String with length."""
    return "".join(choice(ascii_letters + digits) for _ in range(length))


def utc_datetime(**addons: int) -> datetime:
    """Get current datetime with option to add additional timedelta."""
    return datetime.now(tz=timezone.utc) + timedelta(**addons)


def utc_datetime_iso(**addons: int) -> str:
    """Get current datetime in ISO format with option to add additional timedelta."""
    return utc_datetime(**addons).isoformat()


def utc_timestamp(**addons: int) -> int:
    """Get current timestamp with option to add additional timedelta."""
    return int(utc_datetime(**addons).timestamp())


def populate_yaml_specs(app: FastAPI) -> None:
    """Populate yaml specs."""

    @app.get("/openapi.yaml", include_in_schema=False)
    @lru_cache
    def read_openapi_yaml() -> Response:
        openapi_json = app.openapi()
        yaml_s = StringIO()
        ydump(openapi_json, yaml_s)
        return Response(yaml_s.getvalue(), media_type="text/yaml")


__all__ = [
    "Emailer",
    "SendGridEmailer",
    "random_string",
    "utc_datetime",
    "utc_timestamp",
    "log_dumps",
    "log_entry",
    "log_exit",
    "logger",
    "populate_yaml_specs",
]
