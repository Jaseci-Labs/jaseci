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
        print(self.mem)
        return self.get_obj_from_store(obj_id)

    def get_obj_from_store(self, obj_id: UUID | str) -> Architype:
        print("get_obj_from_store in memory", obj_id, self.mem)
        ret = self.mem.get(obj_id, None)
        print(ret)
        return ret

    def has_obj(self, obj_id: UUID | str) -> bool:
        return self.has_obj_in_store(obj_id)

    def has_obj_in_store(self, obj_id: UUID | str) -> bool:
        return obj_id in self.mem

    def save_obj(self, item: Architype) -> None:
        print("saving object", item)
        self.mem[item._jac_.id] = item
        self.save_obj_list.add(item)
        self.commit()

    def commit(self) -> None:
        pass
