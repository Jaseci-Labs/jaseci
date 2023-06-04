from jaseci.extens.api.interface import Interface
from jaseci.extens.api.jsorc_api import JsOrcApi as CoreJsOrcApi
from jaseci_serv.base.jsorc_loadtest import JsorcLoadTest


class JsOrcApi(CoreJsOrcApi):
    @Interface.admin_api()
    def jsorc_loadtest(
        self,
        test: str,
        experiment: str = "",
        mem: int = 0,
        policy: str = "all_local",
        experiment_duration: int = 180,
        eval_phase: int = 10,
        perf_phase: int = 100,
    ):
        """
        A jsorc loadtest
        """
        tester = JsorcLoadTest(test)
        return tester.run_test(
            experiment, mem, policy, experiment_duration, eval_phase, perf_phase
        )
