from enum import Enum, auto


class ref(Enum):
    SELF = auto()
    ENTRY_ACT_IDS = auto()
    EXIT_ACT_IDS = auto()
    ACTIV_ACT_IDS = auto()
    STOPPED = auto()
    RESULT_OUT = auto()
    TMP1 = auto()
    TMP2 = auto()
    TMP3 = auto()

    # Walker refs
    HERE_ID = auto()
    STEP = auto()
    IN_ENT_EXIT = auto()
    NEXT_N_IDS = auto()
    IGNORE_N_IDS = auto()
    DESTROY_N_IDS = auto()

    # Arhcitype refs
