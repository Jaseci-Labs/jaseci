from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.actions.live_actions import load_module_actions, unload_module
import pytest


class ParaphraseModule(CoreTest):
    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(ParaphraseModule, cls).setUpClass()
        ret = load_module_actions("jac_nlp.t5_phraser")
        assert ret == True

    @pytest.mark.order(1)
    @jac_testcase("paraphraser.jac", "test_paraphrase")
    def test_t5_paraphraser(self, ret):
        self.assertGreater(len(ret["report"][0]), 0)

    @classmethod
    def tearDownClass(cls):
        super(ParaphraseModule, cls).tearDownClass()
        ret = unload_module("jac_nlp.t5_phraser.paraphraser")
        assert ret == True
