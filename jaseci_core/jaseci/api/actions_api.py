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
    def actions_register(self, file: str):
        """
        """
        lact.load_actions(file)

    @interface.admin_api()
    def actions_get(self, name: str, value: str):
        """
        """

    @interface.admin_api()
    def actions_list(self, name: str = ''):
        """
        """
        actions = list(lact.live_actions.keys())
        if(not len(name)):
            return actions
        else:
            return list(filter(lambda a: a.startswith(name), actions))

    @interface.admin_api()
    def actions_delete(self, name: str, value: str):
        """
        """
