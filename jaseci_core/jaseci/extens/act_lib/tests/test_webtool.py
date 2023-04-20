from jaseci.utils.test_core import CoreTest, jac_testcase


class WebtoolTest(CoreTest):
    """UnitTest for Webtool"""

    fixture_src = __file__

    @jac_testcase("webtool.jac", "get_meta_valid")
    def test_get_meta_valid(self, ret):
        self.assertTrue(ret["success"])
        expected_tags = set(["og:image", "og:type", "og:title"])
        tags = set(
            [
                meta["property"] if "property" in meta else ""
                for meta in ret["report"][0]
            ]
        )
        self.assertTrue(tags.issuperset(expected_tags))

    @jac_testcase("webtool.jac", "get_meta_need_auth")
    def test_get_meta_need_auth(self, ret):
        self.assertTrue(ret["success"])
        self.assertTrue(len(ret["report"][0]) > 0)

    @jac_testcase("webtool.jac", "get_meta_invalid")
    def test_get_meta_invalid(self, ret):
        self.assertTrue("Failed at getting metadata" in ret["report"][0])

    @jac_testcase("webtool.jac", "get_meta_timeout")
    def test_get_meta_timeout(self, ret):
        self.assertTrue("Failed at getting metadata" in ret["report"][0])

    @jac_testcase("webtool.jac", "get_meta_need_header")
    def test_get_meta_need_header(self, ret):
        self.assertTrue(ret["success"])
        expected_tags = set(["og:image", "og:type", "og:title"])
        tags = set(
            [
                meta["property"] if "property" in meta else ""
                for meta in ret["report"][0]
            ]
        )
        self.assertTrue(tags.issuperset(expected_tags))
