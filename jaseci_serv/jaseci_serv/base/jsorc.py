from jaseci.api.interface import Interface
from jaseci.api.jsorc_api import JsOrcApi as CoreJsOrcApi
from .jsorc_loadtest import JsorcLoadTest


class JsOrcApi(CoreJsOrcApi):
    @Interface.admin_api()
    def jsorc_loadtest(
        self,
        test: str,
        experiment: str = "",
        mem: int = 0,
        policy: str = "all_local",
        experiment_duration: int = 180
    ):
        """
        A jsorc loadtest
        """
        tester = JsorcLoadTest(test)
        return tester.run_test(experiment, mem, policy, experiment_duration)
