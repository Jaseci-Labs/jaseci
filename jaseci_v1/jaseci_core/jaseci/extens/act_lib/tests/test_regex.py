from jaseci.utils.test_core import CoreTest, jac_testcase


class RegexTest(CoreTest):
    """UnitTest for Regex Module"""

    fixture_src = __file__

    @jac_testcase("regex.jac", "findall_test")
    def test_findall(self, ret):
        ret1 = [ret["report"][0][0]]
        ret2 = [ret["report"][0][1]]
        self.assertEqual(ret1, [("width", "20")])
        self.assertEqual(ret2, [("height", "10")])

    @jac_testcase("regex.jac", "search_test")
    def test_search(self, ret):
        ret = ret["report"]
        self.assertEqual(ret, [{"span": (5, 7), "match": "ai"}])

    @jac_testcase("regex.jac", "match_test")
    def test_match(self, ret):
        ret = ret["report"]
        self.assertEqual(ret, [{"span": (0, 1), "match": "T"}])

    @jac_testcase("regex.jac", "fullmatch_test")
    def test_fullmatch(self, ret):
        ret = ret["report"]
        self.assertEqual(ret, [{"span": (0, 16), "match": "THEQUICKBROWNFOX"}])

    @jac_testcase("regex.jac", "split_test")
    def test_split(self, ret):
        ret = ret["report"]
        self.assertEqual(ret, [["Words", "words", "words", ""]])

    @jac_testcase("regex.jac", "finditer_test")
    def test_finditer(self, ret):
        ret = ret["report"]
        self.assertEqual(
            ret,
            [[{"span": (0, 4), "match": "Blue"}, {"span": (13, 17), "match": "Blue"}]],
        )

    @jac_testcase("regex.jac", "sub_test")
    def test_sub(self, ret):
        ret = ret["report"]
        self.assertEqual(ret, ["Account Number - NN, Amount - NN.NN"])

    @jac_testcase("regex.jac", "subn_test")
    def test_subn(self, ret):
        ret = ret["report"]
        self.assertEqual(ret, [["Account Number - NN, Amount - NN.NN", 3]])

    @jac_testcase("regex.jac", "escape_test")
    def test_escape(self, ret):
        ret = ret["report"]
        self.assertEqual(ret, ["https://www\\.jaseci\\.org"])

    @jac_testcase("regex.jac", "purge_test")
    def test_purge(self, ret):
        self.assertEqual(ret["success"], True)
