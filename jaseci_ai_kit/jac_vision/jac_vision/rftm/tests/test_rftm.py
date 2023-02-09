from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.actions.live_actions import load_module_actions, unload_module


class RFTMModule(CoreTest):
    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(RFTMModule, cls).setUpClass()
        ret = load_module_actions("jac_vision.rftm")
        assert ret == True

    @jac_testcase("rftm.jac", "test_predict_anomaly_b64")
    def test_predict_anomaly_b64(self, ret):
        self.assertGreaterEqual(ret["report"][0], 0)

    @jac_testcase("rftm.jac", "test_predict_anomaly")
    def test_predict_anomaly(self, ret):
        self.assertGreaterEqual(ret["report"][0], 0)

    @classmethod
    def tearDownClass(cls):
        super(RFTMModule, cls).tearDownClass()
        ret = unload_module("jac_vision.rftm.rftm")
        assert ret == True
