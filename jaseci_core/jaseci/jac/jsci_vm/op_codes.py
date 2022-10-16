from enum import IntEnum, auto
from jaseci.graph.edge import Edge
from jaseci.graph.node import Node


class JsOp(IntEnum):
    PUSH_SCOPE = auto()
    POP_SCOPE = auto()
    ADD = auto()
    SUB = auto()
    LOAD_CONST = auto()  # [type, bytes, (val)] / [type, (val)] / [type=type, type]
    LOAD_VAR = auto()  # [bytes, (name)]
    REPORT = auto()  # [type, bytes, (val)]
    ACTION_CALL = auto()
    DEBUG_INFO = auto()  # [bytes, line, bytes, (jacfile)]


class JsAttr(IntEnum):
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


type_map = {
    JsAttr.TYPE: type,
    JsAttr.INT: int,
    JsAttr.FLOAT: float,
    JsAttr.STRING: str,
    JsAttr.LIST: list,
    JsAttr.DICT: dict,
    JsAttr.BOOL: bool,
    JsAttr.NULL: None,
    JsAttr.NODE: Node,
    JsAttr.EDGE: Edge,
}
