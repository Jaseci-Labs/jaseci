"""Jaseci Utilities."""

import logging
from datetime import datetime, timedelta, timezone
from random import choice
from string import ascii_letters, digits
from typing import Optional, Union, cast, get_args, get_origin


def random_string(length: int) -> str:
    """Generate String with length."""
    return "".join(choice(ascii_letters + digits) for _ in range(length))


def utc_datetime(**addons: int) -> datetime:
    """Get current datetime with option to add additional timedelta."""
    return datetime.now(tz=timezone.utc) + timedelta(**addons)


def utc_timestamp(**addons: int) -> int:
    """Get current timestamp with option to add additional timedelta."""
    return int(utc_datetime(**addons).timestamp())


def make_optional(cls: type) -> type:
    """Check if the type hint is Optional."""
    # An Optional type will be represented as Union[type, NoneType]
    if get_origin(cls) is Union and type(None) in get_args(cls):
        return cls
    return cast(type, Optional[cls])


logger = logging.getLogger(__name__)
# logger.addHandler(logging.StreamHandler(sys.stdout))
