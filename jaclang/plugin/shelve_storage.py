"""
Shelve storage for persistence storage of jaclang runtime objects
"""

from uuid import UUID, uuid4
import shelve

from jaclang.core.construct import Architype, NodeAnchor
from jaclang.plugin.memory import Memory


class ShelveStorage(Memory):
    storage: shelve.Shelf | None = None

    def __init__(self, session: str = ""):
        super().__init__()
        if session:
            self.connect(session)

    def get_obj_from_store(self, obj_id: UUID | str) -> Architype:
        print("ShelveStorage.get_obj_from_store", obj_id)
        obj = super().get_obj_from_store(obj_id)
        print("obj is", obj)
        if obj is None and self.storage:
            print("======i am losing my mind")
            obj = self.storage.get(str(obj_id), None)
            print("===loading from shelve", obj_id, obj)
            if obj is not None:
                self.mem[obj_id] = obj

        return obj

    def has_obj_in_store(self, obj_id: UUID | str) -> bool:
        return obj_id in self.mem or (
            str(obj_id) in self.storage if self.storage else False
        )

    def commit(self) -> None:
        if self.storage is not None:
            for obj in self.save_obj_list:
                print("===commiting to shelve", obj, obj._jac_.id)
                self.storage[str(obj._jac_.id)] = obj
        self.save_obj_list.clear()

    def connect(self, session: str) -> None:
        self.session = session
        self.storage = shelve.open(session)

    def close(self) -> None:
        print("closing shelve")
        self.commit()
        self.storage.close()
        self.storage = None


# Storage = ShelveStorage()
# Storage.load("jaclang.session")
