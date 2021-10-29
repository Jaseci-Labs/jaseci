from enum import Enum, auto


class op(Enum):
    # NOOP = auto()
    IDS_CLEAR = auto()  # [ref id_list]
    IDS_ADD_OBJ = auto()  # [ref ids, ref obj]
    IDS_GET_LEN = auto()  # [ref dest, ref ids]
    PUSH_SCOPE_W = auto()  # []
    POP_SCOPE = auto()  # []
    SET_LIVE_VAR = auto()  # [str dest, ref value, md_index]
    SET_REF_VAR = auto()  # [ref dest, ref src]
    SET_REF_VARI = auto()  # [ref dest, imm value]
    CREATE_CTX_VAR = auto()  # [ref obj, str dest, ref val, bool is_private]
    SET_ANCHOR = auto()  # [ref obj, str name]
    B_NEQ = auto()  # [ref src1, ref src2, label]
    B_NEQI = auto()  # [ref src1, imm val, label]
    B_NIT = auto()  # [ref src1, typ, label]
    B_A = auto()  # [label]
    PLUS = auto()  # [dest, src, src]
    END = auto()   # []
