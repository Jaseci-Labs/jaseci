from jaseci.svc.actions_optimizer.actions_state import ActionsState
from jaseci.utils.utils import logger


class ActionsOptimizerPolicy:
    """
    Template for action optimizer policy
    """

    def __init__(self) -> None:
        self.actions_state = None
        pass

    def set_actions_state(self, actions_state: ActionsState):
        self.actions_state = actions_state

    def check(self):
        pass


class DefaultPolicy(ActionsOptimizerPolicy):
    """
    Default action optimizer policy, i.e. no automatic optimization
    """

    def check(self):
        pass


class BackAndForthPolicy(ActionsOptimizerPolicy):
    """
    A policy mostly for testing purpose. It will switch one action module back and forth between local and remote every jsorc interval
    """

    def __init__(self, module) -> None:
        self.module = module
        super().__init__()

    def check(self):
        logger.info("IN BACK AND FORTH POLICY")
        change_state = self.actions_state.get_change_set()
        logger.info(change_state)
        if self.module in self.actions_state.get_change_set():
            return
        else:
            cur_state = self.actions_state.get_state(self.module)
            logger.info(cur_state)
            if cur_state is None:
                logger.info("STARTING with remote")
                self.actions_state.set_change_set(self.module, "remote")
            elif cur_state["mode"] == "local":
                logger.info("switch from local to remote")
                self.actions_state.set_change_set(self.module, "remote", "START")
                self.actions_state.set_change_set(
                    self.module, "local", "STOP_WHEN_READY"
                )
            elif cur_state["mode"] == "remote":
                logger.info("switch from remote to local")
                self.actions_state.set_change_set(self.module, "local", "START")
                self.actions_state.set_change_set(self.module, "remote", "STOP")
