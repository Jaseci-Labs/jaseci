from .test_api_core import core_test


class walker_api_test(core_test):
    """Unit tests for Jac Walker APIs"""

    def test_walker_yield(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("walker_yield.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield"}])
        self.assertEqual(ret["report"], [7])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield"}])
        self.assertEqual(ret["report"], [8])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield"}])
        self.assertEqual(ret["report"], [9])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield"}])
        self.assertEqual(ret["report"], [10])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield"}])
        self.assertEqual(ret["report"], ["should start over now"])
        ret = self.call(self.mast, ["walker_run", {"name": "test_yield"}])
        self.assertEqual(ret["report"], [7])

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
