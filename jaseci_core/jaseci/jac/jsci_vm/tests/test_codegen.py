from jaseci.utils.test_core import CoreTest


class TestCodegen(CoreTest):
    """Unit tests for Jac Walker APIs"""

    fixture_src = __file__

    def test_walker_yield(self):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("simple.jac")}],
        )
        self.call(self.mast, ["walker_run", {"name": "most_basic"}])
