"""Jaseci's object abstraction."""
from datetime import datetime
from uuid import UUID, uuid4


class Element:
    """Base class for every object in Jaseci."""

    def __init__(self: "Element", uuid: UUID = None, persist: bool = False) -> None:
        """Initialize element."""
        self.uuid = uuid4() if uuid is None else uuid
        self.timestamp = datetime.now()
        self.persist = persist

    @property
    def id(self: "Element") -> str:
        """Return id of element."""
        return self.uuid
