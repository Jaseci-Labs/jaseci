from jaseci.utils.test_core import CoreTest, jac_testcase


class RequestTests(CoreTest):
    """Unit tests for STD library language"""

    fixture_src = __file__

    @jac_testcase("request.jac", "sample")
    def test_request_trigger(self, ret):
        reports = ret["report"]
        report: dict = reports[0]

        self.assertEqual(200, report.get("status_code"))
        self.assertIsNotNone(response := report.get("response"))
        self.assertEqual(1, response["id"])
        self.assertEqual("iPhone 9", response["title"])

        report: dict = reports[1]

        self.assertEqual(200, report.get("status_code"))
        self.assertIsNotNone(response := report.get("response"))
        self.assertEqual(101, response["id"])
        self.assertEqual("Testing", response["title"])

        report: dict = reports[2]

        self.assertEqual(200, report.get("status_code"))
        self.assertIsNotNone(response := report.get("response"))
        self.assertEqual(1, response["id"])
        self.assertEqual("Testing2", response["title"])
