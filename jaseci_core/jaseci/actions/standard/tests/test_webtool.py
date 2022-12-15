from jaseci.utils.test_core import CoreTest, jac_testcase


class WebtoolTest(CoreTest):
    """UnitTest for Webtool"""

    fixture_src = __file__

    @jac_testcase("webtool.jac", "get_meta_valid")
    def test_get_meta_valid(self, ret):
        self.assertTrue(ret["success"])
        self.assertTrue("og" in ret["report"][0])
        self.assertTrue("meta" in ret["report"][0])
        self.assertTrue("dc" in ret["report"][0])
        self.assertTrue("page" in ret["report"][0])

    @jac_testcase("webtool.jac", "get_meta_invalid")
    def test_get_meta_invalid(self, ret):
        self.assertFalse(ret["success"])
