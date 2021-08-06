from enum import Enum, auto


class ref(Enum):
    SELF = auto()


class w_ref(ref):
    HERE_ID = auto()
    STEP = auto()
    IN_ENT_EXIT = auto()
    STOPPED = auto()
    NEXT_NODE_IDS = auto


# class a_ref(Enum):
