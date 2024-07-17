"""Jaseci FastAPI Types."""

from dataclasses import field
from typing import List

from fastapi import UploadFile as File

OptFile = File | None
Files = List[File]
OptFiles = Files | None


class Defaults:
    """Field Default Handler."""

    NONE = None
    LIST: list = field(default_factory=list)
    DICT: dict = field(default_factory=dict)
    SET: set = field(default_factory=set)
    BYTES: bytes = field(default_factory=bytes)
    STR: str = field(default_factory=str)
