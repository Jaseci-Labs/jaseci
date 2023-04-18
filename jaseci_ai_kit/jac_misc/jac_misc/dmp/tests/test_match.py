from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.jsorc.live_actions import load_module_actions, unload_module


class MatchTest(CoreTest):
    """UnitTest for Match Module"""

    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(MatchTest, cls).setUpClass()
        ret = load_module_actions("jac_misc.match")
        assert ret

    @jac_testcase("match.jac", "get_match_test")
    def test_get_match(self, ret):
        self.assertEqual(ret["report"][0], 0)

    @jac_testcase("match.jac", "match_dist_test")
    def test_match_dist(self, ret):
        self.assertEqual(ret["report"][0], 23)

    @classmethod
    def tearDownClass(cls):
        super(MatchTest, cls).tearDownClass()
        ret = unload_module("jac_misc.match.match")
        assert ret
