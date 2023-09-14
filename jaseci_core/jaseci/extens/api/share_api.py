"""
Object sharing APIs
"""
from jaseci.extens.api.interface import Interface
from jaseci.prim.element import Element


class ShareApi:
    """
    Sharing APIs.
    """

    def __init__(self):
        self.incoming = {}
        self.outgoing = {}

    @Interface.private_api()
    def share_object(
        self, receiver: str, objs: list[Element] = [], read_only: bool = True
    ):
        """
        Sharing an object with a user
        obj: The list of elements to share
        receiver: master of the receiving user
        read_only: if set true, the object shared will be shared as read-only
        """
        # Get the master by id
        # use get_obj with override
        receiver_mast = self._h.get_obj(
            caller_id=self.id, item_id=receiver, override=True
        )

        # Grant the necessary permission to the new user
        self.object_perms_grant(obj, receiver_mast, read_only=read_only)

        # Have the receiver receiving the object
        receiver_mast.incoming[str(obj.id)] = [obj, self]
        receiver_mast.save()

        self.outgoing[str(obj.id)] = [obj, receiver]

        return {"object": str(obj), "sharer": str(self), "receiver": str(receiver_mast)}

    @Interface.private_api()
    def retrieve_shared_object(self, obj_id: str, copy: bool = True):
        """
        Retrieve a shared object from the incoming list and remove it from the list
        """
        try:
            obj, _ = self.incoming.pop(obj_id)
            if copy:
                return obj.duplicate()
            else:
                return obj
        except Exception:
            return None

    @Interface.private_api()
    def share_get_incomings(self):
        """
        Get the incoming objects
        """
        return self.incoming.keys()

    @Interface.private_api()
    def share_get_outgoings(self):
        """
        Get the list of outgoing objects
        """
        return self.outgoing.keys()
