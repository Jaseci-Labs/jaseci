"""
Gins thread which can be attached when rubn with the --gins option.

This is a placeholder for the Jac Gins thread. It is not yet implemented.
"""

from threading import Thread

# from typing import Optional


class GinSThread:
    """Jac Gins thread."""

    def __init__(self) -> None:
        """Create ExecutionContext."""
        self.ghost_thread: Thread = Thread(target=self.worker)
        self.__is_alive: bool = False
        self.start_gins()

    def start_gins(self) -> None:
        """Attach the Gins thread to the Jac machine state."""
        self.__is_alive = True
        self.ghost_thread.start()

    def worker(self) -> None:
        """Worker thread for Gins."""
        # print("Gins thread started")
