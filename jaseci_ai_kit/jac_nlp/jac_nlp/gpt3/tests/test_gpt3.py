from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.actions.live_actions import load_module_actions, unload_module
import pytest


class GPT3Tests(CoreTest):
    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(GPT3Tests, cls).setUpClass()
        ret = load_module_actions("jac_nlp.gpt3")
        assert ret == True

    def test_generate(self):
        self.assertEqual(1, 1)  # TODO: implement the test for gpt3 generate

    @classmethod
    def tearDownClass(cls):
        super(GPT3Tests, cls).tearDownClass()
        ret = unload_module("jac_nlp.gpt3.gpt3")
        assert ret == True
