from enum import Enum


class AppState(Enum):
    FAILED = -2
    DISABLED = -1
    NOT_STARTED = 0
    STARTED = 1
    RUNNING = 2

    def is_ready(self):
        return self == AppState.NOT_STARTED

    def is_running(self):
        return self == AppState.RUNNING

    def has_failed(self):
        return self == AppState.FAILED
