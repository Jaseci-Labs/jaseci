"""Core constructs for Jac Language."""

from __future__ import annotations

import shelve
from uuid import UUID

from .architype import Architype


class Memory:
    """Memory module interface."""

    mem: dict[UUID, Architype] = {}
    save_obj_list: dict[UUID, Architype] = {}

    def __init__(self) -> None:
        """init."""
        pass

    def get_obj(self, obj_id: UUID) -> Architype | None:
        """Get object from memory."""
        return self.get_obj_from_store(obj_id)

    def get_obj_from_store(self, obj_id: UUID) -> Architype | None:
        """Get object from the underlying store."""
        ret = self.mem.get(obj_id)
        return ret

    def has_obj(self, obj_id: UUID) -> bool:
        """Check if the object exists."""
        return self.has_obj_in_store(obj_id)

    def has_obj_in_store(self, obj_id: UUID) -> bool:
        """Check if the object exists in the underlying store."""
        return obj_id in self.mem

    def save_obj(self, item: Architype, persistent: bool) -> None:
        """Save object."""
        self.mem[item._jac_.id] = item
        if persistent:
            # TODO: check if it needs to be saved, i.e. dirty or not
            self.save_obj_list[item._jac_.id] = item

    def commit(self) -> None:
        """Commit changes to persistent storage, if applicable."""
        pass

    def close(self) -> None:
        """Close any connection, if applicable."""
        self.mem.clear()


class ShelveStorage(Memory):
    """Shelve storage for jaclang runtime object."""

    storage: shelve.Shelf | None = None

    def __init__(self, session: str = "") -> None:
        """Init shelve storage."""
        super().__init__()
        if session:
            self.connect(session)

    def get_obj_from_store(self, obj_id: UUID) -> Architype | None:
        """Get object from the underlying store."""
        obj = super().get_obj_from_store(obj_id)
        if obj is None and self.storage:
            obj = self.storage.get(str(obj_id))
            if obj is not None:
                self.mem[obj_id] = obj

        return obj

    def has_obj_in_store(self, obj_id: UUID | str) -> bool:
        """Check if the object exists in the underlying store."""
        return obj_id in self.mem or (
            str(obj_id) in self.storage if self.storage else False
        )

    def commit(self) -> None:
        """Commit changes to persistent storage."""
        if self.storage is not None:
            for obj_id, obj in self.save_obj_list.items():
                self.storage[str(obj_id)] = obj
        self.save_obj_list.clear()

    def connect(self, session: str) -> None:
        """Connect to storage."""
        self.session = session
        self.storage = shelve.open(session)

    def close(self) -> None:
        """Close the storage."""
        super().close()
        self.commit()
        if self.storage:
            self.storage.close()
        self.storage = None
