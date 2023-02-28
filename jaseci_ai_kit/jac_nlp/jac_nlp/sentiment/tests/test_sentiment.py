import pytest

from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.actions.live_actions import load_module_actions, unload_module


class TextSentimentModule(CoreTest):
    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(TextSentimentModule, cls).setUpClass()
        ret = load_module_actions("jac_nlp.sentiment")
        assert ret == True

    @pytest.mark.order(1)
    @jac_testcase("sentiment.jac", "test_predict")
    def test_predict(self, ret):
        self.assertEqual(ret["success"], True)

    @classmethod
    def tearDownClass(cls):
        super(TextSentimentModule, cls).tearDownClass()
        ret = unload_module("jac_nlp.sentiment.sentiment")
        assert ret == True
