from enum import Enum, auto


class JsOp(Enum):
    PUSH_SCOPE = auto()
    POP_SCOPE = auto()
    PUSH = auto()
    ADD = auto()
    LOAD_CONST = auto()
    LOAD_NAME = auto()
    REPORT = auto()
    ACTION_CALL = auto()


class JsAttr(Enum):
    INT = auto()
