from jaseci.extens.api.interface import Interface
from jaseci.extens.api.jsorc_api import JsOrcApi as CoreJsOrcApi
from jaseci_serv.base.jsorc_loadtest import JsorcLoadTest


class JsOrcApi(CoreJsOrcApi):
    @Interface.admin_api()
    def jsorc_loadtest(
        self, test: str, experiment: str = "", mem: int = 0, policy: str = "all_local"
    ):
        """
        A jsorc loadtest
        """
        tester = JsorcLoadTest(test)
        return tester.run_test(experiment, mem, policy)
