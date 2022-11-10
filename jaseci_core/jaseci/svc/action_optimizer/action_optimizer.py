class ActionConfigs:
    def __init__(self) -> None:
        self.configs = {}

    def get_action_config(self, action, mode):
        pass


class ActionOptimizerPolicy:
    def __init__(self) -> None:
        pass


class ActionOptimizer:
    def __init__(self, kube) -> None:
        self.action_states = {}
        self.action_configs = {}
        self.kube = kube
        pass

    def run(self):
        """
        The main optimization function.
        This gets invoked by JSROC regularly at a configured interval.
        """
        pass

    def apply_layout(self, new_layout):
        """
        Apply a new action layout.
        """
        pass

    def spawn_remote(self, name):
        """
        Spawn a microservice through the kube service
        """
        pass

    def load_action(self, name, mode):
        """
        Load an action
        Mode: local, remote or auto
        """
        pass

    def unload_action(self, name):
        """
        Unload an action
        """
        pass

    def remote_action_ready_check(self, name):
        """
        Check if a remote action is ready by querying the action_spec endpoint
        """
        pass
