"""Jaseci's object abstraction."""
from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4


from jaseci.core.memory import Memory


class AccessMode(Enum):
    """Access mode for elements."""

    PUBLIC_READ = 0
    PUBLIC_WRITE = 1
    PRIVATE = 2


class Element:
    """Base class for every object in Jaseci."""

    def __init__(
        self: "Element",
        owner_id: UUID,
        memory: Memory,
        id: UUID = None,
        persist: bool = False,
    ) -> None:
        """Initialize element."""
        self.id = uuid4() if id is None else id
        self.timestamp = datetime.now()
        self.persist = persist
        self.access_default = AccessMode.PRIVATE
        self.rw_access = set()
        self.ro_access = set()
        self.owner_id = owner_id
        self._memory = memory

    def make_public_read(self: "Element") -> None:
        """Make element publically readable."""
        self.access_default = AccessMode.PUBLIC_READ

    def make_public_write(self: "Element") -> None:
        """Make element publically writable."""
        self.access_default = AccessMode.PUBLIC_WRITE

    def make_private(self: "Element") -> None:
        """Make element private."""
        self.access_default = AccessMode.PRIVATE

    def is_public_read(self: "Element") -> bool:
        """Check if element is publically readable."""
        return self.access_default == AccessMode.PUBLIC_READ

    def is_public_write(self: "Element") -> bool:
        """Check if element is publically writable."""
        return self.access_default == AccessMode.PUBLIC_WRITE

    def is_private(self: "Element") -> bool:
        """Check if element is private."""
        return self.access_default == AccessMode.PRIVATE

    def is_readable(self: "Element", caller_id: UUID) -> bool:
        """Check if element is readable by caller."""
        return (
            caller_id == self.owner_id
            or self.is_public_read()
            or caller_id in self.ro_access
            or caller_id in self.rw_access
        )

    def is_writable(self: "Element", caller_id: UUID) -> bool:
        """Check if element is writable by caller."""
        return (
            caller_id == self.owner_id
            or self.is_public_write()
            or caller_id in self.rw_access
        )

    def give_access(self: "Element", caller_id: UUID, read_only: bool = True) -> None:
        """Give access to caller."""
        if read_only:
            self.ro_access.add(caller_id)
        else:
            self.rw_access.add(caller_id)

    def revoke_access(self: "Element", caller_id: UUID) -> None:
        """Revoke access from caller."""
        self.ro_access.discard(caller_id)
        self.rw_access.discard(caller_id)
