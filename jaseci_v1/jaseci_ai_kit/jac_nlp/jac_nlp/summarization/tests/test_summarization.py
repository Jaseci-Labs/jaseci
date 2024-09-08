from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.jsorc.live_actions import load_module_actions, unload_module


class SummarizationTests(CoreTest):
    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(SummarizationTests, cls).setUpClass()
        ret = load_module_actions("jac_nlp.summarization")
        assert ret is True

    @jac_testcase("summarization.jac", "test_summarize_single")
    def test_summarize_single(self, ret):
        self.assertEqual(len(ret["report"][0]), 1)

    @jac_testcase("summarization.jac", "test_summarize_single_percentage")
    def test_summarize_single_percentage(self, ret):
        self.assertEqual(len(ret["report"][0]), 1)

    @jac_testcase("summarization.jac", "test_summarize_url")
    def test_summarize_url(self, ret):
        self.assertEqual(len(ret["report"][0]), 1)

    @jac_testcase("summarization.jac", "test_summarize_batch")
    def test_summarize_batch(self, ret):
        self.assertEqual(len(ret["report"][0]), 3)

    @classmethod
    def tearDownClass(cls):
        super(SummarizationTests, cls).tearDownClass()
        ret = unload_module("jac_nlp.summarization.summarization")
        assert ret is True
