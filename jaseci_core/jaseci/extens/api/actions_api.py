"""
Admin Global api functions as a mixin
"""
from jaseci.extens.api.interface import Interface
import jaseci.jsorc.live_actions as lact
import json


class ActionsApi:
    """
    APIs to manage actions

    This set action APIs enable the manual management of Jaseci actions and action
    libraries/sets. Action libraries can be loaded locally into the running instance of
    the python program, or as a remote container linked action library. In this mode,
    action libraries operate as micro-services. Jaseci will be able to dynamically
    and automatically make this decision for the user based on online monitoring and
    performance profiling.
    """

    @Interface.admin_api(cli_args=["file"])
    def actions_load_local(self, file: str, ctx: dict = {}):
        """
        Hot load a python module and assimilate any Jaseci Actions

        This API will dynamically load a module based on a python file. The module
        is loaded directly into the running Jaseci python instance. This API also
        makes an attempt to auto detect and hot load any python package dependencies
        the file may reference via python's relative imports. This file is assumed to
        have the necessary annotations and decorations required by Jaseci to recognize
        its actions.

        :param file: The python file with full to load actions from.
            (i.e., ~/local/myact.py)
        """
        success = lact.load_local_actions(file, ctx=ctx)
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

    @Interface.admin_api(cli_args=["url"])
    def actions_load_remote(self, url: str, ctx: dict = {}):
        """
        Hot link to a container linked action library

        This API will dynamically load a set of actions that are present on a remote
        server/micro-service. This server must be configured to interact with Jaseci
        properly. This is easily achieved using the same decorators used for local
        action libraries. Remote actions allow for higher flexibility in the languages
        supported for action libraries. If an  library writer would like to use another
        language, the main hook REST api simply needs to be implemented. Please
        refer to documentation on creating action libraries for more details.

        :param url: The url of the API server supporting Jaseci actions.
        """
        success = lact.load_remote_actions(url, ctx=ctx)
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

    @Interface.admin_api(cli_args=["mod"])
    def actions_load_module(self, mod: str, ctx: dict = {}):
        """
        Hot load a python module and assimilate any Jaseci Actions

        This API will dynamically load a module using python's module import format.
        This is particularly useful for pip installed action libraries as the developer
        can directly reference the module using the same format as a regular python
        import. As with load local, the module will be loaded directly into the running
        Jaseci python instance.

        :param mod: The import style module to load actions from.
            (i.e., jaseci_ai_kit.bi_enc)
        """
        success = lact.load_module_actions(mod, ctx=ctx)
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

    @Interface.admin_api()
    def actions_list(self, name: str = ""):
        """
        List a set of or all loaded jaseci actions

        This API is used to list the loaded actions active in Jaseci. These actions
        include all types of loaded actions whether it be local modules or remote
        containers. A particular set of actions can be viewed using the name parameter.

        :param name: The name for a library for which to filter the view of shown
            actions. If left blank all actions from all loaded sets will be shown.
        """
        actions = list(lact.live_actions.keys())
        if len(name):
            actions = list(filter(lambda a: a.startswith(name), actions))
        return actions

    @Interface.admin_api()
    def actions_module_list(self, detailed: bool = False):
        """
        List all modules loaded for actions
        """
        if not detailed:
            action_mods = list(lact.live_action_modules.keys())
        else:
            action_mods = lact.live_action_modules
        return action_mods

    @Interface.admin_api(cli_args=["name"])
    def actions_unload_module(self, name: str):
        """
        Unload modules loaded for actions
        """
        return {"success": lact.unload_module(name)}

    @Interface.admin_api(cli_args=["name"])
    def actions_unload_action(self, name: str):
        """
        Unload modules loaded for actions
        """
        return {"success": lact.unload_action(name)}

    @Interface.admin_api(cli_args=["name"])
    def actions_unload_actionset(self, name: str):
        """
        Unload modules loaded for actions
        """
        return {"success": lact.unload_actionset(name)}

    @Interface.admin_api(cli_args=["name"])
    def actions_call(self, name: str, ctx: dict = {}):
        """
        Call an action by name
        """
        ret, sucess = lact.call_action(name, ctx=ctx)
        return {"success": sucess, "result": ret}
