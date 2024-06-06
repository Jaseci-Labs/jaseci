"""Memory abstraction for jaseci plugin."""

from uuid import UUID

from jaclang.core.construct import Architype


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
