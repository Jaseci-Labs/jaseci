"""Jaseci Utilities."""

import logging
from datetime import datetime, timedelta, timezone
from random import choice
from string import ascii_letters, digits

from .mail import Emailer, SendGridEmailer


def random_string(length: int) -> str:
    """Generate String with length."""
    return "".join(choice(ascii_letters + digits) for _ in range(length))


def utc_datetime(**addons: int) -> datetime:
    """Get current datetime with option to add additional timedelta."""
    return datetime.now(tz=timezone.utc) + timedelta(**addons)


def utc_timestamp(**addons: int) -> int:
    """Get current timestamp with option to add additional timedelta."""
    return int(utc_datetime(**addons).timestamp())


logger = logging.getLogger(__name__)
# logger.addHandler(logging.StreamHandler(sys.stdout))

__all__ = [
    "Emailer",
    "SendGridEmailer",
    "random_string",
    "utc_datetime",
    "utc_timestamp",
    "logger",
]
