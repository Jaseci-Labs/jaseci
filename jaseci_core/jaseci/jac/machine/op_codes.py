from enum import Enum, auto


class op(Enum):
    # NOOP = auto()  # Params:
    IDS_CLEAR = auto()  # Params: [id_list / jac_set]
    IDS_ADD_OBJ = auto()
    PUSH_SCOPE_W = auto()  # Params:
    POP_SCOPE = auto()  # Params:
    SET_LIVE_VAR = auto()  # Params: [dest name, value]
    SET_REF_VAR = auto()  # Params: [dest var, value]
    # GET_LIVE_VAR = auto()  # Params:
    # B_EQ = auto()  # Params: [src1, src2, label]
    # Branch not equal: [src1, src2, label]
    B_NEQ = auto()
    # Branch not is type - [src1, src2, label]
    B_NIT = auto()
    # Branch always - [label]
    B_A = auto()
    # B_RET = auto()  # Params:
    # Plus equal - [dest, src, src]
    PLUS = auto
    END = auto()  # Params:
