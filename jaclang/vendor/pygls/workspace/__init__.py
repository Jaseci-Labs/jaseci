from typing import List
import warnings

from lsprotocol import types

from .workspace import Workspace
from .text_document import TextDocument
from .position import Position

Workspace = Workspace
TextDocument = TextDocument
Position = Position

# For backwards compatibility
Document = TextDocument


def utf16_unit_offset(chars: str):
    warnings.warn(
        "'utf16_unit_offset' has been deprecated, use "
        "'Position.utf16_unit_offset' instead",
        DeprecationWarning,
        stacklevel=2,
    )
    _position = Position()
    return _position.utf16_unit_offset(chars)


def utf16_num_units(chars: str):
    warnings.warn(
        "'utf16_num_units' has been deprecated, use "
        "'Position.client_num_units' instead",
        DeprecationWarning,
        stacklevel=2,
    )
    _position = Position()
    return _position.client_num_units(chars)


def position_from_utf16(lines: List[str], position: types.Position):
    warnings.warn(
        "'position_from_utf16' has been deprecated, use "
        "'Position.position_from_client_units' instead",
        DeprecationWarning,
        stacklevel=2,
    )
    _position = Position()
    return _position.position_from_client_units(lines, position)


def position_to_utf16(lines: List[str], position: types.Position):
    warnings.warn(
        "'position_to_utf16' has been deprecated, use "
        "'Position.position_to_client_units' instead",
        DeprecationWarning,
        stacklevel=2,
    )
    _position = Position()
    return _position.position_to_client_units(lines, position)


def range_from_utf16(lines: List[str], range: types.Range):
    warnings.warn(
        "'range_from_utf16' has been deprecated, use "
        "'Position.range_from_client_units' instead",
        DeprecationWarning,
        stacklevel=2,
    )
    _position = Position()
    return _position.range_from_client_units(lines, range)


def range_to_utf16(lines: List[str], range: types.Range):
    warnings.warn(
        "'range_to_utf16' has been deprecated, use "
        "'Position.range_to_client_units' instead",
        DeprecationWarning,
        stacklevel=2,
    )
    _position = Position()
    return _position.range_to_client_units(lines, range)
