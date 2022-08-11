"""
Admin Global api functions as a mixin
"""
from jaseci.api.interface import interface
import jaseci.actions.live_actions as lact
import json


class actions_api:
    """
    APIs to manage actions

    The set action APIs enable the manual management of Jaseci actions and action
    libraries/sets. Action libraries can be loaded locally into the running instance of
    the python program, or as a remote container linked action library. In this mode,
    action libraries operate as micro-services. Jaseci will be able to dynamically
    and automatically make this decision for the user based on online monitoring and
    performance profiling.
    """

    @interface.admin_api(cli_args=["file"])
    def actions_load_local(self, file: str):
        """
        Hot load a python module and assimlate any Jaseci Actions

        This API will dynamically load a module based on a python file. This API also
        makes an attempt to auto detect and hot load any python package dependencies
        the file may reference via python's relative imports. This file is assumed to
        have the necessary annotations and decorations required by Jaseci to recognize
        its actions.

        :param file: The python file to load actions from.
        """
        success = lact.load_local_actions(file)
        if success:
            cur_config = self.config_get("ACTION_SETS")
            if cur_config and (not isinstance(cur_config, list)):
                config = json.loads(cur_config)
                if file not in config["local"]:
                    config["local"].append(file)
                    self.config_set("ACTION_SETS", json.dumps(config))
            else:
                self.config_set(
                    "ACTION_SETS",
                    json.dumps({"local": [file], "remote": [], "module": []}),
                )
        return {"success": success}

    @interface.admin_api(cli_args=["url"])
    def actions_load_remote(self, url: str):
        """
        Hot load an actions set from live pod at URL
        """
        success = lact.load_remote_actions(url)
        if success:
            cur_config = self.config_get("ACTION_SETS")
            if cur_config and (not isinstance(cur_config, list)):
                config = json.loads(cur_config)
                if url not in config["remote"]:
                    config["remote"].append(url)
                    self.config_set("ACTION_SETS", json.dumps(config))
            else:
                self.config_set(
                    "ACTION_SETS",
                    json.dumps({"local": [], "remote": [url], "module": []}),
                )
        return {"success": success}

    @interface.admin_api(cli_args=["mod"])
    def actions_load_module(self, mod: str):
        """
        Hot load an actions set from live pod at URL
        """
        success = lact.load_module_actions(mod)
        if success:
            cur_config = self.config_get("ACTION_SETS")
            if cur_config and (not isinstance(cur_config, list)):
                config = json.loads(cur_config)
                if mod not in config["module"]:
                    config["module"].append(mod)
                    self.config_set("ACTION_SETS", json.dumps(config))
            else:
                self.config_set(
                    "ACTION_SETS",
                    json.dumps({"local": [], "remote": [], "module": [mod]}),
                )
        return {"success": success}

    # @interface.admin_api()
    # def actions_get(self, name: str, value: str):
    #     """
    #     """

    @interface.admin_api()
    def actions_list(self, name: str = ""):
        """
        List all live jaseci actions
        """
        actions = list(lact.live_actions.keys())
        if len(name):
            actions = list(filter(lambda a: a.startswith(name), actions))
        return actions

    # @interface.admin_api()
    # def actions_delete(self, name: str, value: str):
    #     """
    #     """
