from enum import Enum, auto


class ref(Enum):
    SELF = auto()
    STOPPED = auto()
    RESULT_OUT = auto()


class w_ref(ref):
    HERE_ID = auto()
    STEP = auto()
    IN_ENT_EXIT = auto()
    NEXT_N_IDS = auto()
    IGNORE_N_IDS = auto()


# class a_ref(Enum):
