from .test_api_core import core_test


class walker_api_test(core_test):
    """Unit tests for Jac Walker APIs"""

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
        self.logger_on()
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("walker_yield.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "deep_yield"}])
        self.log(ret["report"])
