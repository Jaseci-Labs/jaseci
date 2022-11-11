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

    def if_changing(self):
        return len(self.change_set) > 0

    def get_change_set(self):
        return self.change_set

    def local_action_loaded(self, name):
        self.state[name]["mode"] = "local"
        del self.change_set[name]["local"]
        if len(self.change_set[name]) == 0:
            del self.change_set[name]

    def local_action_unloaded(self, name):
        del self.change_set[name]["local"]

    def remote_action_loaded(self, name):
        self.state[name]["mode"] = "remote"
        self.state[name]["remote"]["status"] = "READY"
        del self.change_set[name]["remote"]
        if len(self.change_set[name]) == 0:
            del self.change_set[name]

    def remote_action_unloaded(self, name):
        del self.change_set[name]["remote"]

    def start_remote_action(self, name, url):
        if name not in self.state:
            self.state[name] = {}
        self.state[name]["remote"] = {"status": "STARTING", "url": url}
        logger.info("START REMOTE ACTION")
        logger.info(self.state)

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
