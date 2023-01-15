from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.actions.live_actions import load_module_actions, unload_module


class BartSumTests(CoreTest):
    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(BartSumTests, cls).setUpClass()
        ret = load_module_actions("jac_nlp.bart_sum")
        assert ret == True

    @jac_testcase("bart_sum.jac", "test_summarize_single")
    def test_summarize_single(self, ret):
        self.assertEqual(len(ret["report"][0]), 1)

    @jac_testcase("bart_sum.jac", "test_summarize_url")
    def test_summarize_url(self, ret):
        self.assertEqual(len(ret["report"][0]), 1)

    @jac_testcase("bart_sum.jac", "test_summarize_batch")
    def test_summarize_batch(self, ret):
        self.assertEqual(len(ret["report"][0]), 3)

    @classmethod
    def tearDownClass(cls):
        super(BartSumTests, cls).tearDownClass()
        ret = unload_module("jac_nlp.bart_sum.bart_sum")
        assert ret == True
