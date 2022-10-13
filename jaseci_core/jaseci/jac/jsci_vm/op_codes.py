from enum import IntEnum, auto


class JsOp(IntEnum):
    PUSH_SCOPE = auto()
    POP_SCOPE = auto()
    ADD = auto()
    SUB = auto()
    LOAD_CONST = auto()  # [type, bytes, (val)] / [type=type, type]
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
    NODE = auto()
    EDGE = auto()
