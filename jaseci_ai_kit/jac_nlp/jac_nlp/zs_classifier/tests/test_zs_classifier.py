from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.actions.live_actions import load_module_actions, unload_module
import pytest


class ZS_Classifier_Test(CoreTest):
    fixture_src = __file__
    """
    Test Class for ZS_Classifier Module to test the functionality of api's
    """

    @classmethod
    def setUpClass(cls):
        super(ZS_Classifier_Test, cls).setUpClass()
        ret = load_module_actions("jac_nlp.zs_classifier")
        assert ret is True

    @pytest.mark.order(1)
    @jac_testcase("zs_classifier.jac", "test_zs_classify")
    def test_zs_classify(self, ret):
        self.assertEqual(ret["success"], True)

    @classmethod
    def tearDownClass(cls):
        super(ZS_Classifier_Test, cls).tearDownClass()
        ret = unload_module("jac_nlp.zs_classifier.zs_classifier")
        assert ret is True
