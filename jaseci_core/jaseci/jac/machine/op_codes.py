from enum import Enum, auto

class op_code(Enum):
    NOOP = auto()
    PUSH_SCOPE = auto()
    POP_SCOPE = auto()
    SET_LOCAL_VAR = auto()
    SET_CTX_VAR = auto()
