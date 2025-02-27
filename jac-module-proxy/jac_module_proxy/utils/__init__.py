"""Utilities."""

from logging import StreamHandler, getLogger
from os import getenv
from sys import stdout

logger = getLogger(__name__)
logger.setLevel(getenv("LOGGER_LEVEL", "DEBUG"))
logger.addHandler(StreamHandler(stdout))
