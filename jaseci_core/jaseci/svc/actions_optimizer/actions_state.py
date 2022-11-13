from jaseci.utils.utils import logger


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
        Switching set format:
        [
            "ACTION_NAME": {
                "local": "START|STOP|STOP_WHEN_READY",
                "remote": "START|STARTING|STOP|STOP_WHEN_READY"
           }
        ]
        """
        self.state = {}
        self.change_set = {}

    def init_state(self, name):
        """
        Initialize the data structure for the action state tracking for a specific action
        """
        self.state[name] = {
            "mode": None,
            "module": {"name": None},
            "local": {"path": None},
            "remote": {"url": None, "status": None},
        }

        return self.state[name]

    def if_changing(self):
        return len(self.change_set) > 0

    def get_change_set(self):
        return self.change_set

    def local_action_loaded(self, name):
        self.state[name]["mode"] = "local"
        del self.change_set[name]["local"]
        if len(self.change_set[name]) == 0:
            del self.change_set[name]

    def module_action_loaded(self, name, module):
        self.state[name]["mode"] = "module"
        self.state[name]["module"]["name"] = module

    def module_action_unloaded(self, name):
        self.state[name]["module"] = {"name": None}

    def local_action_unloaded(self, name):
        del self.change_set[name]["local"]

    def remove_remote(self, name):
        self.state[name]["remote"] = {"url": None, "status": None}

    def remote_action_loaded(self, name):
        self.state[name]["mode"] = "remote"

    def remote_action_unloaded(self, name):

        if name in self.change_set:
            if "remote" in self.change_set[name]:
                del self.change_set[name]["remote"]
            if len(self.change_set[name]) == 0:
                del self.change_set[name]

    def start_remote_service(self, name, url):
        self.state[name]["remote"] = {"status": "STARTING", "url": url}

    def set_remote_action_ready(self, name):
        self.state[name]["remote"]["status"] = "READY"

    def remote_action_started(self, name):
        self.change_set[name]["remote"] = "STARTING"

    def stop_remote_action(self, name):
        self.state[name]["remote"] = {}
        del self.change_set[name]["remote"]
        if len(self.change_set[name]) == 0:
            del self.change_set[name]

    def get_remote_url(self, name):
        if name not in self.state or "remote" not in self.state[name]:
            return None
        return self.state[name]["remote"].get("url", None)

    def get_state(self, name):
        return self.state.get(name, None)

    def set_url(self, name, url):
        if name not in self.state:
            self.state[name] = {}
        if "remote" not in self.state[name]:
            self.state[name]["remote"] = {}
        self.state[name]["remote"]["url"] = url

    def set_change_set(self, name, mode, status="START"):
        if name not in self.change_set:
            self.change_set[name] = {}
        if mode not in self.change_set[name]:
            self.change_set[name][mode] = status
