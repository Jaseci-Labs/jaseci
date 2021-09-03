"""
Object api as a mixin
"""
from jaseci.element import element


class object_api():
    """Object APIs for generalized operations on Jaseci objects

    ...
    """

    def api_object_get(self, obj: element, depth: int = 0,
                       detailed: bool = False):
        """Returns object details for any Jaseci object.

        """
        return obj.serialize(deep=depth, detailed=detailed)

    def api_object_perms_get(self, obj: element):
        """Returns object access mode for any Jaseci object.

        """
        return {'access': obj.j_access}

    def api_object_perms_set(self, obj: element, mode: str):
        """Sets object access mode for any Jaseci object.

        """
        valid_perms = ['public', 'private', 'read_only']
        ret = {}
        if(mode not in valid_perms):
            ret['success'] = False
            ret['response'] = f'{mode} not valid, must be in {valid_perms}'
        else:
            getattr(obj, 'make_'+mode)()
            ret['success'] = True
            ret['response'] = f'{obj} set to {mode}'
        return ret

    def api_object_perms_grant(self, obj: element, mast: element,
                               read_only: bool = False):
        """Grants another user permissions to access a Jaseci object.

        """
        granted = obj.give_access(mast, read_only=read_only)
        ret = {'success': granted}
        if(granted):
            ret['response'] = f'Access to {obj} granted to {mast}'
        else:
            ret['response'] = f'Cannot grant {mast} access to {obj}'
        return ret

    def api_object_perms_revoke(self, obj: element, mast: element):
        """Remove permissions for user to access a Jaseci object.

        """
        revoked = obj.remove_access(mast)
        ret = {'success': revoked}
        if(revoked):
            ret['response'] = f'Access to {obj} revoked from {mast}'
        else:
            ret['response'] = f'{mast} did not have access to {obj}'
        return ret
