class ActionsState:
    """
    An object tracking the various states of available actions. Utilized by the ActionsOptimizer and ActionsOptimizerPolicy
    """

    def __init__(self):
        """
        Actions state format:
        actions_state = {
            "ACTION_NAME": {
                "mode": "local|remote",
                "module": {
                    "name": MDOULE_NAME
                },
                "local": {
                    "path": LOCAL MODULE FILE PATH
                },
                "remote": {
                    "url": "remote_url of the action microservice",
                    "status": "READY|STARTING|RETIRING"
                }
            }
        }
        """
        self.state = {}

    def init_state(self, name):
        """
        Initialize the data structure for the action state tracking for a specific action
        """
        self.state[name] = {
            "mode": None,
            "module": {"name": None, "loaded_module": None},
            "local": {"path": None},
            "remote": {"url": None, "status": None},
        }

        return self.state[name]

    def get_active_actions(self):
        """
        Return list of action modules currently used
        """
        return list(self.state.keys())

    def local_action_loaded(self, name):
        self.state[name]["mode"] = "local"

    def module_action_loaded(self, name, module, loaded):
        self.state[name]["mode"] = "module"
        self.state[name]["module"]["name"] = module
        self.state[name]["module"]["loaded_module"] = loaded

    def module_action_unloaded(self, name):
        self.state[name]["mode"] = None
        self.state[name]["module"]["name"] = None

    def remote_action_unloaded(self, name):
        self.state[name]["mode"] = None

    def remove_remote(self, name):
        self.state[name]["remote"] = {"url": None, "status": None}

    def remote_action_loaded(self, name):
        self.state[name]["mode"] = "remote"

    def start_remote_service(self, name, url):
        self.state[name]["remote"] = {"status": "STARTING", "url": url}

    def set_remote_action_ready(self, name):
        self.state[name]["remote"]["status"] = "READY"

    def stop_remote_action(self, name):
        self.state[name]["remote"] = {}

    def get_remote_url(self, name):
        if name not in self.state or "remote" not in self.state[name]:
            return None
        return self.state[name]["remote"].get("url", None)

    def get_all_state(self):
        ret = {}
        for name, state in self.state.items():
            ret[name] = {"mode": state["mode"]}
        return ret

    def get_state(self, name):
        return self.state.get(name, None)

    def set_url(self, name, url):
        if name not in self.state:
            self.state[name] = {}
        if "remote" not in self.state[name]:
            self.state[name]["remote"] = {}
        self.state[name]["remote"]["url"] = url
