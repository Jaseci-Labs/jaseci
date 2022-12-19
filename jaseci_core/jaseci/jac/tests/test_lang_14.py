from jaseci.utils.test_core import CoreTest


class Lang14Test(CoreTest):
    """Unit tests for Jac Walker APIs"""

    fixture_src = __file__

    def test_free_reference(self):
        self.logger_on()
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("fam.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "free_ref"}])
        self.assertTrue(ret["success"])
