from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.actions.live_actions import load_module_actions, unload_module


class DPTModule(CoreTest):
    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(DPTModule, cls).setUpClass()
        ret = load_module_actions("jac_vision.dpt")
        assert ret == True

    @jac_testcase("dpt.jac", "test_estimate")
    def test_estimate(self, ret):
        self.assertEqual(ret["success"], True)

    @jac_testcase("dpt.jac", "test_estimate_batch")
    def test_estimate_batch(self, ret):
        self.assertEqual(ret["success"], True)

    @classmethod
    def tearDownClass(cls):
        super(DPTModule, cls).tearDownClass()
        ret = unload_module("jac_vision.dpt.dpt")
        assert ret == True
