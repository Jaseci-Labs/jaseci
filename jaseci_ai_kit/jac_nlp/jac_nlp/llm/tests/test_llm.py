from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.jsorc.live_actions import load_module_actions, unload_module
import pytest


class LLMTests(CoreTest):
    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(LLMTests, cls).setUpClass()
        ret = load_module_actions("jac_nlp.llm", ctx={"model_name": "gpt2"})
        assert ret == True

    @jac_testcase("llm.jac", "test_generate")
    @pytest.mark.skip(reason="Not working on Github Actions")
    def test_generate(self, ret):
        self.assertEqual(ret["success"], True)

    @classmethod
    def tearDownClass(cls):
        super(LLMTests, cls).tearDownClass()
        ret = unload_module("jac_nlp.llm.llm")
        assert ret == True
