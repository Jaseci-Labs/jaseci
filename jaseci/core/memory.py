"""Element memory class for Jaseci."""
import sys
from typing import TypeVar
from uuid import UUID


Element = TypeVar("Element")


class Memory:
    """Memory class for Jaseci."""

    def __init__(self: "Memory") -> None:
        """Initialize memory."""
        self.mem = {}
        self._machine = None
        self.save_obj_list = set()

    def get_obj(
        self: "Memory", caller_id: UUID, item_id: UUID, override: bool = False
    ) -> "Element":
        """Get item from memory by id, then try store."""
        ret = self.mem.get(item_id, None)
        if override or (ret is not None and ret.is_readable(caller_id)):
            return ret

    def has_obj(self: "Memory", item_id: UUID) -> bool:
        """Check if item is in memory."""
        return item_id in self.mem.keys()

    def save_obj(self: "Memory", caller_id: UUID, item: "Element") -> None:
        """Save item to memory."""
        if item.is_writable(caller_id):
            self.mem[item.id] = item
            if item._persist:
                self.save_obj_list.add(item)

    def destroy_obj(self: "Memory", caller_id: UUID, item: "Element") -> None:
        """Destroy item from memory."""
        if item.is_writable(caller_id):
            self.mem.pop(item.id)
            if item._persist:
                self.save_obj_list.remove(item)

    # Utility functions
    # -----------------
    def get_object_distribution(self: "Memory") -> dict:
        """Get distribution of objects in memory."""
        dist = {}
        for i in self.mem.keys():
            t = type(self.mem[i])
            if t in dist.keys():
                dist[t] += 1
            else:
                dist[t] = 1
        return dist

    def mem_size(self: "Memory") -> float:
        """Get size of memory in KB."""
        return sys.getsizeof(self.mem) / 1024
