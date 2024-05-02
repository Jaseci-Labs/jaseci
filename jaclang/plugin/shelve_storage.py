"""
Shelve storage for persistence storage of jaclang runtime objects
"""

from uuid import UUID, uuid4
import shelve

from jaclang.core.construct import Architype, NodeAnchor
from jaclang.plugin.memory import Memory


class ShelveStorage(Memory):
    def __init__(self):
        super().__init__()

    def get_obj_from_store(self, obj_id: UUID | str) -> Architype:
        print("in shelve_storage.py:get_obj_from_store")
        obj = super().get_obj_from_store(obj_id)
        print("got obj as", obj)
        if obj is None:
            obj = self.shelve.get(str(obj_id), None)
            print("in get_obj_from_store")
            print(obj)
            if obj is not None:
                self.mem[obj_id] = obj
                return obj

        return obj

    def has_obj_in_store(self, obj_id: UUID | str) -> bool:
        return obj_id in self.mem or str(obj_id) in self.shelve

    def commit(self) -> None:
        for obj in self.save_obj_list:
            print("writing to storage", obj._jac_.id, obj)
            self.shelve[str(obj._jac_.id)] = obj
        self.save_obj_list.clear()
        print("currently in self.mem:", self.mem)

    def load(self, session: str) -> None:
        self.shelve = shelve.open(session)


Storage = ShelveStorage()
Storage.load("jaclang.session")
