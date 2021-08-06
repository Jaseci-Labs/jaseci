from enum import Enum, auto


class ref(Enum):
    SELF = auto()


class w_ref(ref):
    HERE_ID = auto()
    STEP = auto()


# class a_ref(Enum):