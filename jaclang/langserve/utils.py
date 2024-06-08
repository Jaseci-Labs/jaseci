"""Utility functions for the language server."""

import logging

from jaclang.vendor.pygls.server import LanguageServer

import lsprotocol.types as lspt


def log_error(ls: LanguageServer, message: str) -> None:
    """Log an error message."""
    ls.show_message_log(message, lspt.MessageType.Error)
    ls.show_message(message, lspt.MessageType.Error)


def log(info: str) -> None:
    """Log an info message."""
    logging.warning(info)
