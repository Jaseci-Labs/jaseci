from jaseci.utils.test_core import CoreTest, jac_testcase


class DateTest(CoreTest):
    fixture_src = __file__

    @jac_testcase("date.jac", "sample")
    def test_date_syntax(self, ret):
        self.assertEqual(
            ret["report"],
            [
                {
                    "day": 26,
                    "hour": 7,
                    "microsecond": 93606,
                    "minute": 42,
                    "month": 4,
                    "second": 53,
                    "weekday": 3,
                    "year": 2023,
                    "iso": "2023-04-26T07:42:53.093606",
                },
                "2023-06-05T07:42:53.093606",
                "2023-04-26T00:42:53.093606",
            ],
        )
