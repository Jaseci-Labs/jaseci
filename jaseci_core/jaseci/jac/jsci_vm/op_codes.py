from enum import IntEnum, auto
from jaseci.graph.edge import Edge
from jaseci.graph.node import Node


class JsOp(IntEnum):
    PUSH_SCOPE = auto()
    POP_SCOPE = auto()
    ADD = auto()
    SUBTRACT = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    POWER = auto()
    NEGATE = auto()
    COMPARE = auto()
    LOAD_CONST = auto()  # [type, bytes, (val)] / [type, (val)] / [type=type, type]
    LOAD_VAR = auto()  # [bytes, (name)]
    REPORT = auto()  # [type, bytes, (val)]
    ACTION_CALL = auto()
    DEBUG_INFO = auto()  # [bytes, line, bytes, (jacfile)]


class JsType(IntEnum):
    TYPE = auto()
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    LIST = auto()
    DICT = auto()
    BOOL = auto()
    NULL = auto()
    NODE = auto()
    EDGE = auto()


class JsCmp(IntEnum):
    EE = auto()
    LT = auto()
    GT = auto()
    LTE = auto()
    GTE = auto()
    NE = auto()
    IN = auto()
    NIN = auto()
    NOT = auto()


type_map = {
    JsType.TYPE: type,
    JsType.INT: int,
    JsType.FLOAT: float,
    JsType.STRING: str,
    JsType.LIST: list,
    JsType.DICT: dict,
    JsType.BOOL: bool,
    JsType.NULL: None,
    JsType.NODE: Node,
    JsType.EDGE: Edge,
}
