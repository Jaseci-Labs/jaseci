from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.actions.live_actions import load_module_actions, unload_module
import pytest


class BiNERTest(CoreTest):
    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(BiNERTest, cls).setUpClass()
        ret = load_module_actions("jaseci_ai_kit.bi_ner")
        assert ret is True

    @pytest.mark.order(1)
    @jac_testcase("bi_ner.jac", "test_bi_ner_train")
    def test_ner_train(self, ret):
        print(ret)
        self.assertEqual(ret["success"], True)

    @pytest.mark.order(2)
    @jac_testcase("bi_ner.jac", "test_bi_ner_infer")
    def test_biner_infer(self, ret):
        self.assertEqual(ret["success"], True)

    @classmethod
    def tearDownClass(cls):
        super(BiNERTest, cls).tearDownClass()
        ret = unload_module("jaseci_ai_kit.modules.bi_ner.bi_ner")
        assert ret is True
