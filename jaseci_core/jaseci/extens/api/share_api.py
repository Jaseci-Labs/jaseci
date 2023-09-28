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
        # Get the master object by id
        receiver_mast = self._h.get_obj(
            caller_id=self.jid, item_id=receiver, override=True
        )

        for obj in objs:
            # Grant read-only permission to the new user
            self.object_perms_grant(obj, receiver_mast, read_only=read_only)
            obj.save()

            # Add the objet id to the receiver's incoming list
            receiver_mast.incoming[str(obj.id)] = {"jid": self.jid, "name": self.name}

        receiver_mast.save()
        self.save()

        return {
            "objects": [str(obj) for obj in objs],
            "sharer": str(self),
            "receiver": str(receiver_mast),
        }

    @Interface.private_api()
    def share_incoming_pop(self, obj_id: str):
        """
        Remove an item from the incoming list
        """
        try:
            self.incoming.pop(obj_id)
            return True
        except Exception:
            return None

    @Interface.private_api()
    def share_incoming_list(self):
        """
        Get the incoming objects
        """
        return self.incoming
