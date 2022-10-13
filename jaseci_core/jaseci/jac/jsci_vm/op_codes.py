from enum import IntEnum, auto


class JsOp(IntEnum):
    PUSH_SCOPE = auto()
    POP_SCOPE = auto()
    ADD = auto()
    SUB = auto()
    LOAD_CONST = auto()
    LOAD_NAME = auto()
    REPORT = auto()
    ACTION_CALL = auto()
    DEBUG_INFO = auto()


class JsAttr(IntEnum):
    INT = auto()
    FLOAT = auto()
    STRING = auto()
    LIST = auto()
    DICT = auto()
    BOOL = auto()
    NODE = auto()
    EDGE = auto()
    TYPE = auto()
