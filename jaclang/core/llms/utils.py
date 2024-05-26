"""Utility functions for the LLMs module."""

try:
    from loguru import logger  # noqa F401
except ImportError:
    import logging

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
