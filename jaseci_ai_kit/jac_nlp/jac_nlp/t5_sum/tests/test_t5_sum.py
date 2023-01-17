from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.actions.live_actions import load_module_actions, unload_module
import pytest


class T5SumTest(CoreTest):
    fixture_src = __file__
    """
    Test Class for T5Sum Module to test the functionality of api's
    """

    @classmethod
    def setUpClass(cls):
        super(T5SumTest, cls).setUpClass()
        ret = load_module_actions("jac_nlp.t5_sum")
        assert ret is True

    @pytest.mark.order(1)
    @jac_testcase("t5_sum.jac", "test_t5_sum_detection")
    def test_t5_sum_detection(self, ret):
        self.assertEqual(ret["success"], True)

    @classmethod
    def tearDownClass(cls):
        super(T5SumTest, cls).tearDownClass()
        ret = unload_module("jac_nlp.t5_sum.t5_sum")
        assert ret is True
