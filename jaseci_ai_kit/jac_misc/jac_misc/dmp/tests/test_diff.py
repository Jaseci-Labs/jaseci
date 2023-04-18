from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.actions.live_actions import load_module_actions, unload_module


class DiffTest(CoreTest):
    """UnitTest for Diff Module"""

    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(DiffTest, cls).setUpClass()
        ret = load_module_actions("jac_nlp.diff")
        assert ret

    @jac_testcase("diff.jac", "get_diff_test")
    def test_get_diff(self, ret):
        self.assertEqual(ret["report"][0], [(-1, "Goo"), (1, "Ba"), (0, "d dog")])

    @jac_testcase("diff.jac", "semantic_clean_test")
    def test_semantic_clean(self, ret):
        self.assertEqual(ret["report"][0], [(-1, "Goo"), (1, "Ba")])

    @jac_testcase("diff.jac", "levsht_0_test")
    def test_levsht_0(self, ret):
        self.assertEqual(ret["report"][0], 0)

    @jac_testcase("diff.jac", "levsht_non0_test")
    def test_levsht_non0(self, ret):
        self.assertNotEqual(ret["report"][0], 0)

    @classmethod
    def tearDownClass(cls):
        super(DiffTest, cls).tearDownClass()
        ret = unload_module("jac_nlp.diff.diff")
        assert ret
