from enum import Enum


class ServiceState(Enum):
    FAILED = -1
    NOT_STARTED = 0
    STARTED = 1
    RUNNING = 2
