from enum import IntEnum, auto
from jaseci.prim.edge import Edge
from jaseci.prim.node import Node


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
    AND = auto()
    OR = auto()
    ASSIGN = auto()
    COPY_FIELDS = auto()
    REPORT = auto()
    ACTION_CALL = auto()
    INCREMENT = auto()  # [type]
    LOAD_CONST = auto()  # [type, bytes, (val)] / [type, (val)] / [type=type, type]
    LOAD_VAR = auto()  # [bytes, (name)]
    CREATE_VAR = auto()  # [bytes, (name)]
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
    PEQ = auto()
    MEQ = auto()
    TEQ = auto()
    DEQ = auto()


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

cmp_op_map = {
    JsCmp.NOT: lambda val: not val,
    JsCmp.EE: lambda v1, v2: v1 == v2,
    JsCmp.LT: lambda v1, v2: v1 < v2,
    JsCmp.GT: lambda v1, v2: v1 > v2,
    JsCmp.LTE: lambda v1, v2: v1 <= v2,
    JsCmp.GTE: lambda v1, v2: v1 >= v2,
    JsCmp.NE: lambda v1, v2: v1 != v2,
    JsCmp.IN: lambda v1, v2: v1 in v2,
    JsCmp.NIN: lambda v1, v2: v1 not in v2,
}
