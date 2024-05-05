"""
Memory abstraction for jaseci plugin
"""

from uuid import UUID, uuid4

from jaclang.core.construct import Architype


class Memory:

    mem = {}
    save_obj_list = set()

    def __init__(self):
        pass

    def get_obj(self, obj_id: UUID | str) -> Architype:
        print("Memory.get_obj", obj_id)
        return self.get_obj_from_store(obj_id)

    def get_obj_from_store(self, obj_id: UUID | str) -> Architype:
        print("Memory.get_obj_from_store", self.mem)
        ret = self.mem.get(obj_id, None)
        print("memory.get_obj_from_store", obj_id, ret)
        return ret

    def has_obj(self, obj_id: UUID | str) -> bool:
        return self.has_obj_in_store(obj_id)

    def has_obj_in_store(self, obj_id: UUID | str) -> bool:
        return obj_id in self.mem

    def save_obj(self, item: Architype, persistent: bool) -> None:
        self.mem[item._jac_.id] = item
        if persistent:
            # TODO: check if it needs to be saved, i.e. dirty or not
            print("adding to save_obj_list", item)
            self.save_obj_list.add(item)
            print("save_obj_list", self.save_obj_list)

    def commit(self) -> None:
        """Commit changes to persistent storage, if applicable"""
        pass

    def close(self) -> None:
        """Close any connection, if applicable"""
        print("((((((((((((((((reseting self.mem))))))))))))))))")
        print("before reseting self.mem", self.mem)
        self.mem.clear()
        print("after reseting self.mem", self.mem)

    def connect(self) -> None:
        """Establish connection with storage, if applicable"""
        pass
