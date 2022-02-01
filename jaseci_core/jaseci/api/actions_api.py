"""
Admin Global api functions as a mixin
"""
from jaseci.api.interface import interface
import jaseci.actions.live_actions as lact


class actions_api():
    """
    Admin global APIs
    """

    @interface.admin_api(cli_args=['file'])
    def actions_load_local(self, file: str):
        """
        Hot load a python module and assimlate any Jaseci Actions
        """
        return {"success": lact.load_local_actions(file)}

    @interface.admin_api(cli_args=['url'])
    def actions_load_remote(self, url: str):
        """
        Hot load an actions set from live pod at URL
        """
        return {"success": lact.load_remote_actions(url)}

    # @interface.admin_api()
    # def actions_get(self, name: str, value: str):
    #     """
    #     """

    @interface.admin_api()
    def actions_list(self, name: str = ''):
        """
        List all live jaseci actions
        """
        actions = list(lact.live_actions.keys())
        if(len(name)):
            actions = list(filter(lambda a: a.startswith(name), actions))
        return actions

    # @interface.admin_api()
    # def actions_delete(self, name: str, value: str):
    #     """
    #     """
