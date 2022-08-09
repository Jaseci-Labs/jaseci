from jaseci.utils.test_core import core_test


class interpreter_test(core_test):
    """Unit tests for Jac Interpreter / Language features"""

    fixture_src = __file__

    def test_has_var_plucking(self):
        ret = self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac("lang_features.jac")}],
        )
        ret = self.call(self.mast, ["walker_run", {"name": "has_var_plucking"}])
        self.assertEqual(ret["report"], [["points_to", "points_to", "points_to"]])
