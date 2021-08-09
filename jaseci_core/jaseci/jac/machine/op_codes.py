from enum import Enum, auto


class op(Enum):
    # NOOP = auto()  # Params:
    IDS_CLEAR = auto()  # Params: [id_list / jac_set]
    IDS_ADD_OBJ = auto()  # [ids, obj]
    IDS_GET_LEN = auto()  # [dest, ids]
    PUSH_SCOPE_W = auto()  # Params:
    POP_SCOPE = auto()  # Params:
    SET_LIVE_VAR = auto()  # Params: [dest name, value]
    SET_REF_VAR = auto()  # Params: [dest var, value]
    CREATE_CTX_VAR = auto()  # Params: [obj, dest name, value, is_private]
    SET_ANCHOR = auto()  # Assign anchor - [obj, name]
    B_NEQ = auto()  # Branch not equal: [src1, src2, label]
    B_NIT = auto()  # Branch not is type - [src1, src2, label]
    B_A = auto()  # Branch always - [label]
    PLUS = auto()  # Plus - [dest, src, src]
    END = auto()   # End execution
