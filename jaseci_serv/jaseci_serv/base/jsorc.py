from jaseci.api.interface import Interface
from jaseci.api.jsorc_api import JsOrcApi as CoreJsOrcApi
from .jsorc_loadtest import JsorcLoadTest


class JsOrcApi(CoreJsOrcApi):
    @Interface.admin_api()
    def jsorc_loadtest(self, test: str, experiment: str = "", mem: int = 0):
        """
        A jsorc loadtest
        """
        tester = JsorcLoadTest(test)
        return tester.run_test(experiment, mem)
