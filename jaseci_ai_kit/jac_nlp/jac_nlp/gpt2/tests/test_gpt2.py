from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.actions.live_actions import load_module_actions, unload_module


class GPT2Tests(CoreTest):
    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(GPT2Tests, cls).setUpClass()
        ret = load_module_actions("jac_nlp.gpt2")
        assert ret == True

    @jac_testcase("gpt2.jac", "test_generate")
    def test_generate(self, ret):
        self.assertEqual(len(ret["report"][0][0]), 5)

    @jac_testcase("gpt2.jac", "test_get_embeddings")
    def test_get_embeddings(self, ret):
        self.assertEqual(len(ret["report"][0]), 2)
        self.assertEqual(len(ret["report"][0][0][0]), 1024)

    @classmethod
    def tearDownClass(cls):
        super(GPT2Tests, cls).tearDownClass()
        ret = unload_module("jac_nlp.gpt2.gpt2")
        assert ret == True
