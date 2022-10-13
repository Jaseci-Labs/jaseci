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


class JsAttr(IntEnum):
    INT = auto()
