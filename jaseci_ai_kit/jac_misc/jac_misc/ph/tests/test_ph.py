from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.actions.live_actions import load_module_actions, unload_module
import pytest


class PHModule(CoreTest):
    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(PHModule, cls).setUpClass()
        ret = load_module_actions("jac_misc.ph")
        assert ret == True

    @pytest.mark.order(1)
    @jac_testcase("ph.jac", "test_create_head_list")
    def test_create_head_list(self, ret):
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(2)
    @jac_testcase("ph.jac", "test_create_head")
    def test_create_head(self, ret):
        self.assertEqual(ret["report"][0], "test_head")

    @pytest.mark.order(3)
    @jac_testcase("ph.jac", "test_predict")
    def test_predict(self, ret):
        self.assertIsInstance(ret["report"][0], int)

    @pytest.mark.order(4)
    @jac_testcase("ph.jac", "test_train")
    def test_train(self, ret):
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(6)
    @jac_testcase("ph.jac", "test_predict_trained")
    def test_predict_trained(self, ret):
        self.assertIsInstance(ret["report"][0], int)

    @classmethod
    def tearDownClass(cls):
        super(PHModule, cls).tearDownClass()
        ret = unload_module("jac_misc.ph.ph")
        assert ret == True
