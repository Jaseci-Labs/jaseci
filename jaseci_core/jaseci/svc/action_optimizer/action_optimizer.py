class ActionConfigs:
    def __init__(self) -> None:
        self.configs = {}

    def get_action_config(self, action, mode):
        pass


class ActionOptimizerPolicy:
    def __init__(self) -> None:
        pass


class ActionOptimizer:
    def __init__(self) -> None:
        self.action_states = {}
        self.action_configs = {}
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

    def load_action(self, action, mode):
        """
        Load an action
        """

    def unload_action(self, action):
        """
        Unload an action
        """

    def remote_action_ready_check(self, action):
        """
        Check if a remote action is ready by querying the action_spec endpoint
        """
