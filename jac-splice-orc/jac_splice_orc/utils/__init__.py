"""Importing required modules and classes."""

from datetime import UTC, datetime, timedelta
from logging import StreamHandler, getLogger
from os import getenv
from sys import stdout


def utc_datetime(**addons: int) -> datetime:
    """Get current datetime with option to add additional timedelta."""
    return datetime.now(tz=UTC) + timedelta(**addons)


def utc_timestamp(**addons: int) -> int:
    """Get current timestamp with option to add additional timedelta."""
    return int(utc_datetime(**addons).timestamp())


logger = getLogger(__name__)
logger.setLevel(getenv("LOGGER_LEVEL", "DEBUG"))
logger.addHandler(StreamHandler(stdout))
