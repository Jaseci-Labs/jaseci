"""
Super (master) api as a mixin
"""


class super_api():
    """Super APIs for creating nicknames for UUIDs and other long strings

    """

    def admin_api_master_createsuper(self, name: str, set_active: bool = True):
        """
        Create a super instance and return root node super object
        """
        mas = self.spawn_super(name)
        if(self.sub_master_ids.has_obj_by_name(name)):
            return {'response': f"{name} already exists"}
        self.sub_master_ids.add_obj(mas)
        return mas.serialize()
