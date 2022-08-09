from jaseci.utils.test_core import core_test
from jaseci.actor.walker import walker


class walker_api_test(core_test):
    """Unit tests for Jac Walker APIs"""

    fixture_src = __file__

    def test_walker_yield(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("walker_yield.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield"}])
        self.assertEqual(ret["report"], ["entering", 7])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield"}])
        self.assertEqual(ret["report"], [8])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield"}])
        self.assertEqual(ret["report"], [9])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield"}])
        self.assertEqual(ret["report"], [10])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield"}])
        self.assertEqual(ret["report"], ["should start over now", "exiting"])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield"}])
        self.assertEqual(ret["report"], ["entering", 7])

    def test_walker_yield_report(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("walker_yield.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield_report"}])
        self.assertEqual(ret["report"], [7])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield_report"}])
        self.assertEqual(ret["report"], [8])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield_report"}])
        self.assertEqual(ret["report"], [9])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield_report"}])
        self.assertEqual(ret["report"], [10])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield_report"}])
        self.assertEqual(ret["report"], ["should start over now"])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield_report"}])
        self.assertEqual(ret["report"], [7])

    def test_walker_yield_disengage(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("walker_yield.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield_disengage"}])
        self.assertEqual(ret["report"], [7])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield_disengage"}])
        self.assertEqual(ret["report"], [8])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield_disengage"}])
        self.assertEqual(ret["report"], [9])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield_disengage"}])
        self.assertEqual(ret["report"], [10])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield_disengage"}])
        self.assertEqual(ret["report"], ["should start over now"])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield_disengage"}])
        self.assertEqual(ret["report"], [7])

    def test_walker_yield_take(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("walker_yield.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield_take"}])
        self.assertEqual(ret["report"], [7, "test"])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield_take"}])
        self.assertEqual(ret["report"], [8, "test"])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield_take"}])
        self.assertEqual(ret["report"], [9, "test"])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield_take"}])
        self.assertEqual(ret["report"], [10, "test"])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield_take"}])
        self.assertEqual(ret["report"], ["should start over now"])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield_take"}])
        self.assertEqual(ret["report"], [7, "test"])

    def test_walker_smart_yield(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("walker_yield.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "smart_yield"}])
        before = self.mast._h.get_object_distribution()
        ret = self.call(self.mast, ["walker_run", {"name": "smart_yield"}])
        ret = self.call(self.mast, ["walker_run", {"name": "smart_yield"}])
        ret = self.call(self.mast, ["walker_run", {"name": "smart_yield"}])
        after = self.mast._h.get_object_distribution()
        self.assertEqual(before, after)
        self.assertEqual(ret["report"], [{"id": 2}])

    def test_walker_smart_yield_no_future(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("walker_yield.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "smart_yield_no_future"}])
        before = self.mast._h.get_object_distribution()
        ret = self.call(self.mast, ["walker_run", {"name": "smart_yield_no_future"}])
        ret = self.call(self.mast, ["walker_run", {"name": "smart_yield_no_future"}])
        ret = self.call(self.mast, ["walker_run", {"name": "smart_yield_no_future"}])
        after = self.mast._h.get_object_distribution()
        self.assertEqual(before, after)
        self.assertEqual(ret["report"], [{}])

    def test_walker_deep_yield(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("walker_yield.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "deep_yield"}])
        self.assertEqual(
            ret["report"],
            [
                {},
                {"id": 0},
                {"id": 1},
                {"id": 2},
                {"id": 3},
                {"id": 4},
                {"id": 5},
                {"id": 6},
                {"id": 7},
                {"id": 8},
                {"id": 9},
                {},
                {"id": 0},
                {"id": 1},
                {"id": 2},
                11,
            ],
        )

    def test_walker_deep_yield2(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("walker_yield.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "deep_yield2"}])
        self.assertEqual(
            ret["report"],
            [
                "entry",
                {},
                {"id": 0},
                {"id": 1},
                {"id": 2},
                {"id": 3},
                {"id": 4},
                {"id": 5},
                {"id": 6},
                {"id": 7},
                {"id": 8},
                {"id": 9},
                "entry",
                {},
                {"id": 0},
                {"id": 10},
                {"id": 1},
                {"id": 11},
            ],
        )

    def test_walker_deep_yield_no_leak(self):
        self.logger_on()
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("walker_yield.jac")}],
        )
        before = self.mast._h.get_object_distribution()[walker]
        self.call(self.mast, ["walker_run", {"name": "deep_yield"}])
        self.call(self.mast, ["walker_run", {"name": "deep_yield"}])
        self.call(self.mast, ["walker_run", {"name": "deep_yield"}])
        after = self.mast._h.get_object_distribution()[walker]
        self.assertEqual(before, after)
