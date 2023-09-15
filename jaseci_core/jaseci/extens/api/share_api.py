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
            caller_id=self.jid, item_id=receiver, override=True
        )

        for obj in objs:
            # Grant the necessary permission to the new user
            self.object_perms_grant(obj, receiver_mast, read_only=read_only)
            obj.save()

            # Have the receiver receiving the object
            receiver_mast.incoming[str(obj.id)] = str(self)

            self.outgoing[str(obj.id)] = str(receiver)

        receiver_mast.save()
        self.save()

        return {
            "objects": [str(obj) for obj in objs],
            "sharer": str(self),
            "receiver": str(receiver_mast),
        }

    @Interface.private_api()
    def share_remove_incoming(self, obj_id: str):
        """
        Remove an item from the incoming list
        """
        try:
            self.incoming.pop(obj_id)
            return True
        except Exception:
            return None

    @Interface.private_api()
    def share_get_incomings(self):
        """
        Get the incoming objects
        """
        return list(self.incoming.keys())

    @Interface.private_api()
    def share_get_outgoings(self):
        """
        Get the list of outgoing objects
        """
        return list(self.outgoing.keys())
