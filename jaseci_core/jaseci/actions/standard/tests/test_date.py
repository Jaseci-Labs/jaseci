from jaseci.utils.test_core import CoreTest


class DateTest(CoreTest):
    """UnitTest for Phrase to date action"""

    fixture_src = __file__

    def test_phrase_to_date(self):
        ret = self.call(
            self.mast, ["sentinel_register", {"code": self.load_jac("date.jac")}]
        )
        ret = self.call(self.mast, ["walker_run", {"name": "phrase_to_date_test"}])
        ret = ret["report"][0]
        self.assertEqual(ret, "2022-05-26")
