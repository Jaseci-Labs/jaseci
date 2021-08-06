from enum import Enum, auto


class op_code(Enum):
    # NOOP = auto()  # Params:
    PUSH_SCOPE_W = auto()  # Params:
    POP_SCOPE = auto()  # Params:
    SET_LIVE_VAR = auto()  # Params: dest name, value
    # GET_LIVE_VAR = auto()  # Params:
    # B_EQ = auto()  # Params: src1, src2, label
    B_NEQ = auto()  # Params: src1, src2, label
    # B_RET = auto()  # Params:
    END = auto()  # Params:
