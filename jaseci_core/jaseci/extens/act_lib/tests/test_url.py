from jaseci.utils.test_core import CoreTest, jac_testcase


class UrlTest(CoreTest):
    fixture_src = __file__

    @jac_testcase("url.jac", "is_valid_test")
    def test_is_valid(self, ret):
        self.assertEqual(
            ret["report"],
            [True, False, False],
        )

    @jac_testcase("url.jac", "ping_test")
    def test_ping(self, ret):
        self.assertEqual(
            ret["report"],
            [True, False, False, False],
        )

    @jac_testcase("url.jac", "download_text_test")
    def test_download_text(self, ret):
        # Download the jaseci homepage as a test
        self.assertGreater(abs(len(ret["report"][0])), 0)

    @jac_testcase("url.jac", "download_b64_test")
    def test_download_b64(self, ret):
        # Jaseci white paper is 2,034,680 bytes in base64
        self.assertEqual(
            len(ret["report"][0]),
            2034680,
        )
