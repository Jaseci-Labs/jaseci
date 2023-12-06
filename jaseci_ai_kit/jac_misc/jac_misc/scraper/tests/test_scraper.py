from jaseci.utils.test_core import CoreTest, jac_testcase
from jaseci.jsorc.live_actions import load_module_actions, unload_module


class ScraperTest(CoreTest):
    fixture_src = __file__

    @classmethod
    def setUpClass(cls):
        super(ScraperTest, cls).setUpClass()
        ret = load_module_actions("jac_misc.scraper")
        assert ret == True

    @jac_testcase("scraper.jac", "test_scraper")
    def test_scraper(self, ret):
        reports = ret["report"]
        self.assertEqual("httpswwwgooglecomsearchqspeedtest", reports[0])

        scraper = reports[1]
        content = scraper["content"]
        self.assertTrue(
            all(
                txt[0] in txt[1]
                for txt in [
                    ["Google Fiber Internet Speed Test", content],
                    ["Two simple internet plans. Fast and Faster", content],
                ]
            )
        )

        self.assertEqual(
            set(
                [
                    "https://fiber.google.com/speedtest/",
                    "https://www.google.com/search?q=speed+test",
                ]
            ),
            set(scraper["scanned"]),
        )

        self.assertEqual(
            set(
                [
                    "https://fiber.google.com/speedtest/",
                    "https://www.google.com/search?q=speed+test",
                ]
            ),
            set(scraper["scraped"]),
        )

    @classmethod
    def tearDownClass(cls):
        super(ScraperTest, cls).tearDownClass()
        ret = unload_module("jac_misc.scraper.scraper")
        assert ret == True
