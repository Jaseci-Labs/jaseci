from .test_api_core import core_test


class walker_api_test(core_test):
    """Unit tests for Jac Walker APIs"""

    def test_walker_yield(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("walker_yield.jac")}],
        )
        ret = self.call(
            self.mast,
            ["walker_run", {"name": "test_yield"}],
        )
        self.log(ret)
