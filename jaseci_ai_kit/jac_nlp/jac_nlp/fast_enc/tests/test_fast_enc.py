from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.actions.live_actions import load_module_actions, unload_module
import pytest


class FastEncTest(CoreTest):
    fixture_src = __file__
    """
    Test Class for Fast encoder Module to test the functionality of api's
    """

    @classmethod
    def setUpClass(cls):
        super(FastEncTest, cls).setUpClass()
        ret = load_module_actions("jac_nlp.fast_enc")
        assert ret is True

    @pytest.mark.order(1)
    @jac_testcase("fast_enc.jac", "test_train")
    def test_train(self, ret):
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(2)
    @jac_testcase("fast_enc.jac", "test_predict")
    def test_predict(self, ret):
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(3)
    @jac_testcase("fast_enc.jac", "test_fast_enc_save_model")
    def test_fast_enc_save_model(self, ret):
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(4)
    @jac_testcase("fast_enc.jac", "test_fast_enc_load_model")
    def test_fast_enc_load_model(self, ret):
        self.assertEqual(ret["success"], True)

    @classmethod
    def tearDownClass(cls):
        super(FastEncTest, cls).tearDownClass()
        ret = unload_module("jac_nlp.fast_enc.fast_enc")
        assert ret is True
