from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.actions.live_actions import load_module_actions, unload_module


class ClSummerModule(CoreTest):
    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(ClSummerModule, cls).setUpClass()
        ret = load_module_actions("jaseci_ai_kit.cl_summer")
        assert ret == True

    @jac_testcase("cl_summer.jac", "test_summarizer_text")
    def test_summarizer_text(self, ret):
        self.assertEqual(len(ret["report"][0]), 1)

    @jac_testcase("cl_summer.jac", "test_summarizer_url")
    def test_summarizer_url(self, ret):
        self.assertEqual(len(ret["report"][0]), 5)

    @classmethod
    def tearDownClass(cls):
        super(ClSummerModule, cls).tearDownClass()
        ret = unload_module("jaseci_ai_kit.modules.cl_summer.cl_summer")
        assert ret == True
